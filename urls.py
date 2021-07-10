from view.task import TaskList, TaskSingle, task_namespace

# add api models to list in format {"root": root, "model": model(Resource)}
TASK_REGISTERED_ROOTS = [
    {"root": "/", "model": TaskList},
    {"root": "/<int:task_id>/", "model": TaskSingle},
]

for model in TASK_REGISTERED_ROOTS:
    task_namespace.add_resource(model["model"], model["root"])
