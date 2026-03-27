from pydantic import BaseModel, Field


class CreateGoalRequest(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = ""


class GoalResponse(BaseModel):
    id: str
    title: str
    description: str
    status: str
    task_ids: list[str] = []


class GoalListResponse(BaseModel):
    goals: list[GoalResponse]
