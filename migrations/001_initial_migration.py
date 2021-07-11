"""

Peewee migrations -- 001_initial_migration.py.

"""

import peewee
from models.task import Task


SQL = peewee.SQL


def migrate(migrator, database, fake=False, **kwargs):
    migrator.create_model(Task)
    migrator.run()


def rollback(migrator, database, fake=False, **kwargs):
    migrator.remove_model(Task)
    migrator.run()
