from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    session_id: str = Field(min_length=1, max_length=128, pattern=r"^[a-zA-Z0-9_\-]+$")
    message: str = Field(min_length=1, max_length=4000)


class ChatResponseSchema(BaseModel):
    response: str
    created_goal_ids: list[str]
    created_task_ids: list[str]
