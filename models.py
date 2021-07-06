"""
The module to describe project classes in a database
"""
from datetime import datetime

from peewee import Model, SqliteDatabase, TextField
from peewee import DateTimeField, CharField, AutoField

import settings


# use temp db in memory while testing
db = SqliteDatabase(settings.DATABASE_NAME)
if settings.TESTING is True:
    db = SqliteDatabase(":memory:")
    db.connect()


class BaseModel():
    """Parent of project database classes."""

    class Meta:
        database = db


class Task(BaseModel):
    """The model to represent small task, uses
    models.BaseModel (for more information see its doc)."""
    id = AutoField()
    title = CharField(max_length=150)
    content = TextField()
    created_at = DateTimeField(default=datetime.now())