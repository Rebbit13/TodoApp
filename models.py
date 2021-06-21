"""
The module to describe project classes in a database
"""
from datetime import datetime

from peewee import Model, SqliteDatabase, TextField
from peewee import DateTimeField, CharField, AutoField

import config


# use temp db in memory while testing
db = SqliteDatabase(config.DATABASE_NAME)
if config.TESTING is True:
    db = SqliteDatabase(":memory:")
    db.connect()


class BaseModel(Model):
    """Parent of project database classes.
    Add SQLite db with name from config to
    class meta.

    Class table will be added to
    db after db create with module create_db.py
    (watch create_db.py doc).

    Uses peewee.Model to connect to a db."""

    class Meta:
        database = db


class Task(BaseModel):
    """The model to represent small task, uses
    models.BaseModel (for more information see its doc)."""
    id = AutoField()
    title = CharField(max_length=150)
    content = TextField()
    created_at = DateTimeField(default=datetime.now())


class Pop(BaseModel):
    id = AutoField()
    title = CharField(max_length=150)