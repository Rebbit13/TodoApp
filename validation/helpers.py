from flask import make_response, request


def validate_if_model_exists(key_name: str, database_model):
    """
    validate if model exist
    if not return resp 404
    :param key_name: name of the id argument (for example task_id),
    which will be passed from path
    :param database_model: peewee model to search in db
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            model = database_model.get_or_none(id=kwargs[key_name])
            if model:
                return func(model, *args, **kwargs)
            else:
                return make_response({"message": f'There is no model with id {kwargs[key_name]}'}, "404")
        return wrapper
    return decorator


def validate_model_input(schema):
    """
    validate if input correct
    if not return resp 400
    :param schema: marshmallow model schema to validate
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            errors = schema().validate(data=request.get_json())
            if errors:
                return make_response(errors, "400")
            else:
                return func(*args, **kwargs)
        return wrapper
    return decorator
