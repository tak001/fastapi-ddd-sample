from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class ChatResponse:
    response: str
    created_goal_ids: tuple[str, ...]
    created_task_ids: tuple[str, ...]


class ChatAgentPort(ABC):
    """Driven port: abstraction for AI agent that processes chat messages."""

    @abstractmethod
    def process_message(self, session_id: str, user_message: str) -> ChatResponse: ...
