from typing import Literal

from pydantic import BaseModel, Field


class CreateTaskRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: str = ""
    goal_id: str | None = None
    priority: Literal["high", "medium", "low"] = "medium"
    due_date: str | None = None


class TaskResponse(BaseModel):
    id: str
    title: str
    description: str
    status: str
    priority: str = "medium"
    goal_id: str | None = None
    due_date: str | None = None


class TaskListResponse(BaseModel):
    tasks: list[TaskResponse]
