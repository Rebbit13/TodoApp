from flask_restx import Resource
from peewee import DoesNotExist
from werkzeug.exceptions import NotFound

from evgeny_todo.api.Models.task import Task
from evgeny_todo.api.Validation.task import TaskCreate, TaskUpdate
from evgeny_todo.utils.validator import Validator

task_create = Validator(TaskCreate)
task_update = Validator(TaskUpdate)


class TaskList(Resource):

    @staticmethod
    def get():
        tasks = [{"id": t.id,
                  "title": t.title,
                  "content": t.content,
                  "created_at": t.created_at}
                 for t in Task.select()]
        return tasks

    @staticmethod
    @task_create.validate_model
    def post(task):
        new_task = Task.create(title=task.title,
                               content=task.content)
        return new_task


class TaskSingle(Resource):

    @staticmethod
    def _get_task(task_id):
        try:
            task = Task.get(id=task_id)
        except DoesNotExist:
            raise NotFound(description=f"There is no task with id {task_id}")
        else:
            return task

    def get(self, task_id):
        return self._get_task(task_id)

    @task_update.validate_model
    def put(self, task_id, task: TaskUpdate):
        task_from_db = self._get_task(task_id)
        task_from_db.title = task.title
        task_from_db.content = task.content
        task_from_db.save()
        return dict(task_from_db)

    def delete(self, task_id):
        task = self._get_task(task_id)
        task.delete_instance()
        return None
