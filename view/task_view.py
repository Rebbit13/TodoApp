from flask import make_response, request
from flask_restx import Resource, Namespace, reqparse

from evgeny_todo.models.task import Task
from evgeny_todo.validation.task import TaskSchema

task_namespace = Namespace('task', description='Task operations')

task_parser = reqparse.RequestParser()
task_parser.add_argument('title', required=True, location='json')
task_parser.add_argument('content', required=True, location='json')


class TaskList(Resource):

    @staticmethod
    def get():
        return [{"id": t.id,
                 "title": t.title,
                 "content": t.content,
                 "created_at": t.created_at}
                for t in Task.select()]

    @staticmethod
    @task_namespace.expect(task_parser, validate=False)
    def post():
        errors = TaskSchema().validate(data=request.get_json())
        if errors:
            return make_response(errors, "400")
        task = TaskSchema().load(request.get_json())
        model = Task.create(title=task.title,
                            content=task.content)
        return make_response(TaskSchema().dumps(model), "201")


class TaskSingle(Resource):
    class Decorator:
        @classmethod
        def check_if_task_exists(cls, func):
            """ if task does not exist return resp 404"""
            def wrapper(task_id, *args, **kwargs):
                model = Task.get_or_none(id=task_id)
                if model:
                    return func(model, *args, **kwargs)
                else:
                    return make_response(f'There is no task with id {task_id}', "404")
            return wrapper

    @staticmethod
    @Decorator.check_if_task_exists
    def get(model):
        return make_response(TaskSchema().dumps(model), "200")

    @staticmethod
    @task_namespace.expect(task_parser, validate=False)
    @Decorator.check_if_task_exists
    def put(model):
        errors = TaskSchema().validate(data=request.get_json())
        if errors:
            return make_response(errors, "400")
        task = TaskSchema().load(request.get_json())
        model.title, model.content = task.title, task.content
        model.save()
        return make_response(TaskSchema().dumps(model), "201")

    @staticmethod
    @Decorator.check_if_task_exists
    def delete(model):
        model.delete_instance()
        return make_response(f"Deleted task with id {model.id}", "200")
