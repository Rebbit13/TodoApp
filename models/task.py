from peewee import TextField, CharField

from models.mixin import BaseMixin, CreatedAtMixin


class Task(BaseMixin, CreatedAtMixin):
    title = CharField(max_length=150)
    content = TextField()
