"""
Main module of the project.
Process http requests.
"""
import json
import logging

from flask import Flask
from flask_restx import fields, Resource, Api, reqparse
from peewee import DoesNotExist, IntegrityError
from werkzeug.exceptions import NotFound, BadRequest

import config
from models import Task


app = Flask(__name__)
api = Api(app, validate=True)


# logging. If config.DEBUG == True print debug information
# in console. Else use logfile path
LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
if config.DEBUG is True:
    logging.basicConfig(level='DEBUG', format=LOG_FORMAT)
else:
    logging.basicConfig(level='INFO',
                        filename=config.LOG_FILE,
                        format=LOG_FORMAT)
logger = logging.getLogger()


# task endpoints
task_api = api.namespace('api/task', description='Task operations')

# model to serialize task for response
task_model = api.model("task",
                       {"id": fields.Integer(),
                        'title': fields.String(max_length=150),
                        'content': fields.String(),
                        'created_at': fields.DateTime()})

# Parser model to validate task in request
task_parser = reqparse.RequestParser()
task_parser.add_argument('title', required=True, location='json')
task_parser.add_argument('content', required=True, location='json')


@task_api.route('')
class TaskList(Resource):
    @task_api.marshal_list_with(task_model, envelope="tasks")
    def get(self):
        """
        method to get all exists tasks
        :return: serialized list of tasks in json
        """
        task = [{"id": t.id,
                 "title": t.title,
                 "content": t.content,
                 "created_at": t.created_at}
                for t in Task.select()]
        return task

    @task_api.expect(task_parser, validate=True)
    @task_api.marshal_with(task_model, envelope="tasks")
    def post(self):
        """
        method to create new task
        :return: response 200 OK with
        serialized task in json
        or 400 Bad Request if missing title
        or content or both
        """
        try:
            if len(api.payload['title']) > 150:
                raise BadRequest("Title length can not be "
                                 "more than 150 chars")
            task = Task.create(title=api.payload['title'],
                               content=api.payload['content'])
        except KeyError:
            raise BadRequest("Missing required attrs")
        except IntegrityError:
            raise BadRequest("Atrs can not be NULL")
        else:
            return task


@task_api.route('/<int:task_id>')
class TaskModel(Resource):
    @staticmethod
    def _get_task(task_id):
        """
        method to get task from db by id
        if task dos not exist rise 404 error in
        response
        :param task_id: task id from src
        :return: task or 404 Not Found
        """
        try:
            task = Task.get(id=task_id)
        except DoesNotExist:
            raise NotFound()
        else:
            return task

    @task_api.marshal_with(task_model, envelope="tasks")
    def get(self, task_id):
        """
        method to get concrete task by id
        :param task_id: task id from src
        :return: response 200 OK with
        serialized task in json
        or 404 Not Found
        """
        return self._get_task(task_id)

    @task_api.expect(task_parser, validate=True)
    @task_api.marshal_with(task_model, envelope="tasks")
    def put(self, task_id):
        """
        method to update concrete task by id
        :param task_id: task id from src
        :return: response 200 OK with
        serialized updated task in json
        or 404 Not Found
        """
        task = self._get_task(task_id)
        task.title = api.payload.get('title', task.title)
        if len(api.payload['title']) > 150:
            raise BadRequest("Title length can not be "
                             "more than 150 chars")
        task.content = api.payload.get('content', task.content)
        task.save()
        return task

    def delete(self, task_id):
        """
        delete task by id
        :param task_id: task id from src
        :return: response 200 OK or 404 Not Found
        """
        task = self._get_task(task_id)
        task.delete_instance()
        return None


if __name__ == '__main__':
    app.run(debug=config.DEBUG)
