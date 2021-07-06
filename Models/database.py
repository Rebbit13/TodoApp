from peewee import SqliteDatabase

import settings

if settings.TESTING is True:
    db = SqliteDatabase(":memory:")
else:
    db = SqliteDatabase(settings.DATABASE_NAME)
