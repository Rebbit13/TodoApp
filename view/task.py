from flask import make_response, request
from flask_restx import Resource, Namespace, reqparse

from models.task import Task
from validation.helpers import validate_if_model_exists, validate_model_input
from validation.task import TaskSchema


# init task namespaces for swagger docs
task_namespace = Namespace('task', description='Task operations')

# init parser for swagger docs
task_parser = reqparse.RequestParser()
task_parser.add_argument('title', required=True, location='json')
task_parser.add_argument('content', required=True, location='json')


class TaskList(Resource):

    @staticmethod
    def get():
        tasks = list(Task.select(Task.id, Task.title, Task.created_at).dicts())
        return TaskSchema(many=True).dump(tasks)

    @staticmethod
    @task_namespace.expect(task_parser, validate=False)
    @validate_model_input(schema=TaskSchema)
    def post():
        task = TaskSchema().load(request.get_json())
        model = Task.create(title=task.title,
                            content=task.content)
        return make_response(TaskSchema().dumps(model), "201")


class TaskSingle(Resource):

    @staticmethod
    @validate_if_model_exists(key_name="task_id", database_model=Task)
    def get(model, *args, **kwargs):
        return make_response(TaskSchema().dumps(model), "200")

    @staticmethod
    @task_namespace.expect(task_parser, validate=False)
    @validate_if_model_exists(key_name="task_id", database_model=Task)
    @validate_model_input(schema=TaskSchema)
    def put(model, *args, **kwargs):
        task = TaskSchema().load(request.get_json())
        model.title, model.content = task.title, task.content
        model.save()
        return make_response(TaskSchema().dumps(model), "201")

    @staticmethod
    @validate_if_model_exists(key_name="task_id", database_model=Task)
    def delete(model, *args, **kwargs):
        model.delete_instance()
        return make_response({"message": f"Deleted task with id {model.id}"}, "200")
