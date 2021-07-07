from pydantic import BaseModel, validator, ValidationError


class TaskAbstract(BaseModel):
    id: int = None
    title: str
    content: str
    created_at: str = None

    @validator("title")
    def check_title_length(cls, v):
        if len(v) > 150:
            raise ValueError("Task title mast not be more than 150 chars")
        return v


class TaskCreate(TaskAbstract):
    pass


class TaskUpdate(TaskAbstract):
    title: str = None
    content: str = None
