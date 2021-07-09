from flask_restx import Namespace

from evgeny_todo.view.task_view import TaskList, TaskSingle, task_namespace

# add api models to list in format {"root": root, "model": model(Resource)}
REGISTERED_ROOTS = [
    {"root": "/", "model": TaskList},
    {"root": "/<int:task_id>/", "model": TaskSingle},
]

for model in REGISTERED_ROOTS:
    task_namespace.add_resource(model["model"], model["root"])
