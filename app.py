import logging

from flask import Flask
from flask_restx import Api

import settings
from evgeny_todo.api.urls import task_namespace
from evgeny_todo.migrations.migrations import migrate_database


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
