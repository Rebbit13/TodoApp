""" module for base project mixins """

from datetime import datetime

from peewee import Model, SqliteDatabase
from peewee import DateTimeField, AutoField

import settings

db = SqliteDatabase(settings.DATABASE_NAME)
if settings.TESTING is True:
    db = SqliteDatabase(":memory:")
    db.connect()


class BaseMixin(Model):
    """Add database to meta and id as auto field"""
    id = AutoField()

    class Meta:
        abstract = True
        database = db


class CreatedAtMixin(Model):
    """Set created_at auto field"""
    created_at = DateTimeField(default=datetime.now())
