""" module for base project mixins """

from datetime import datetime

from peewee import Model
from peewee import DateTimeField, AutoField

from Models.database import db


class BaseMixin(Model):
    """Add database to meta and id as auto field"""
    id = AutoField()

    class Meta:
        abstract = True
        database = db


class CreatedAtMixin(Model):
    """Set created_at auto field"""
    created_at = DateTimeField(default=datetime.now())

    class Meta:
        abstract = True
