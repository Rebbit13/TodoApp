"""
It is a module to create database before first running the app.
Module parse atrs of the class from meta, create db if not
exist and add table.
To add new peewee.Model to a db as a table add it to
REGISTERED_MODELS before first running the app and this module.
CAN ONLY USE BEFORE CREATING THE DB
"""
from peewee import SqliteDatabase

from models import Task, Pop


# add new model here before first running the app and this module
REGISTERED_MODELS = [Task, Pop]


def add_table(models: list):
    """
    add new class to a db from class meta as a table
    :param models: list of peewee.Model
    :return: None
    """
    for model in models:
        db = model.__dict__["_meta"].__dict__["database"]
        db.connect()
        db.create_tables([model])
        db.close()


add_table(REGISTERED_MODELS)
