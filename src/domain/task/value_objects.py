from __future__ import annotations

import datetime
from dataclasses import dataclass
from enum import Enum

from domain.entity_id import EntityId
from domain.task.exceptions import TaskValidationError

TITLE_MAX_LENGTH = 100


class TaskStatus(Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class TaskPriority(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass(frozen=True)
class TaskId(EntityId):
    pass


@dataclass(frozen=True)
class TaskTitle:
    value: str

    def __post_init__(self) -> None:
        if not self.value.strip():
            raise TaskValidationError("Task title must not be empty")
        if len(self.value) > TITLE_MAX_LENGTH:
            raise TaskValidationError(
                f"Task title must not exceed {TITLE_MAX_LENGTH} characters"
            )


@dataclass(frozen=True)
class TaskDueDate:
    value: str

    def __post_init__(self) -> None:
        try:
            datetime.date.fromisoformat(self.value)
        except ValueError:
            raise TaskValidationError(
                f"Task due date must be a valid date in YYYY-MM-DD format, got: {self.value}"
            )
