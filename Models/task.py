from peewee import TextField, CharField

from Models.mixin import BaseMixin, CreatedAtMixin


class Task(BaseMixin, CreatedAtMixin):
    title = CharField(max_length=150)
    content = TextField()
