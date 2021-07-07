import settings
from todo.Models.database import db
from api.Models.task import Task

REGISTERED_MODELS = [Task]


def migrate_database():
    """ Func create db if its not exists and
    migrate registered models. To register
     Model add it to REGISTERED_MODELS  """
    db.connect()
    db.create_tables(REGISTERED_MODELS)
    if settings.TESTING is False:
        db.close()
