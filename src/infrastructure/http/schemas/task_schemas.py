from pydantic import BaseModel, Field


class CreateTaskRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: str = ""


class TaskResponse(BaseModel):
    id: str
    title: str
    description: str
    status: str


class TaskListResponse(BaseModel):
    tasks: list[TaskResponse]
