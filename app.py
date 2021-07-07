import logging

from flask import Flask
from flask_restx import fields, Resource, Api, reqparse
from peewee import DoesNotExist, IntegrityError
from werkzeug.exceptions import NotFound, BadRequest

import settings
from evgeny_todo.api.View.task_view import TaskList
from evgeny_todo.api.urls import task_namespace
from evgeny_todo.todo.Models.migrations import migrate_database
from evgeny_todo.api.Models.task import Task

LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
if settings.DEBUG is True:
    logging.basicConfig(level='DEBUG', format=LOG_FORMAT)
else:
    logging.basicConfig(level='INFO',
                        filename=settings.LOG_FILE,
                        format=LOG_FORMAT)
logger = logging.getLogger()

app = Flask(__name__)
api = Api(app,  prefix='/api', validate=False)

api.add_namespace(task_namespace)


if __name__ == '__main__':
    migrate_database()
    app.run(debug=settings.DEBUG)