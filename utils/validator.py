from flask import request
from pydantic import ValidationError
from werkzeug.exceptions import BadRequest


class Validator:
    def __init__(self, model):
        self.model = model

    def validate_model(self, func):
        def real_decorator(*arqs, **kwargs):
            print(request.get_json())
            try:
                task = self.model.parse_raw(request.get_data())
            except ValidationError as e:
                raise BadRequest(description=e.json())
            except TypeError as e:
                raise BadRequest(description={"message": "There is no data in request"})
            else:
                model = func(task=task, *arqs, **kwargs)
            return model
        return real_decorator
