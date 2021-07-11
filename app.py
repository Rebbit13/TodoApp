import logging
import os

from flask import Flask
from flask_restx import Api

from database import migrate, db
from urls import task_namespace


LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
if bool(os.environ['DEBUG']) is True:
    logging.basicConfig(level='DEBUG', format=LOG_FORMAT)
else:
    logging.basicConfig(level=os.environ['LOG_LEVEL'],
                        filename=os.environ['LOG_FILE'],
                        format=LOG_FORMAT)
logger = logging.getLogger()

db.init(
    database=os.environ['POSTGRES_DB'],
    user=os.environ['POSTGRES_USER'],
    password=os.environ['POSTGRES_PASSWORD'],
    host="database",
    port=os.environ['POSTGRES_PORT'],
    connect_timeout=3)


app = Flask(__name__)
api = Api(app,  prefix='/api', validate=False)
api.add_namespace(task_namespace)


if __name__ == '__main__':
    migrate("initial_migration")
    app.run(debug=bool(os.environ['DEBUG']), host="0.0.0.0")
