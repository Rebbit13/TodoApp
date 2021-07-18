from marshmallow import validate, fields
from marshmallow_peewee import ModelSchema

from models.task import Task


class TaskSchema(ModelSchema):
    title = fields.String(validate=validate.Length(min=1, max=150),
                          required=True)
    content = fields.String(validate=validate.Length(min=1),
                            required=True)

    class Meta:
        model = Task
