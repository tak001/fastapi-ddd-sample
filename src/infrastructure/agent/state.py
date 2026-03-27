from __future__ import annotations

from typing import Annotated

from langgraph.graph.message import add_messages
from typing_extensions import TypedDict


class AgentState(TypedDict):
    """State definition for the goal/task management agent graph."""

    messages: Annotated[list, add_messages]
    session_id: str
    intent: str
    pending_tasks: list[dict[str, str]]
    created_goal_ids: list[str]
    created_task_ids: list[str]
    task_updates: list[dict[str, str]]
