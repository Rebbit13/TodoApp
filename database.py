from peewee_migrate import Router
from playhouse.postgres_ext import PostgresqlExtDatabase

db = PostgresqlExtDatabase(None)


def migrate(migrate_name):
    router = Router(db)
    router.run(migrate_name)
