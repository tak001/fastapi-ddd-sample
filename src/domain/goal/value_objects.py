from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from domain.goal.exceptions import GoalValidationError
from domain.entity_id import EntityId

TITLE_MAX_LENGTH = 200


class GoalStatus(Enum):
    ACTIVE = "active"
    ACHIEVED = "achieved"
    ABANDONED = "abandoned"


@dataclass(frozen=True)
class GoalId(EntityId):
    pass


@dataclass(frozen=True)
class GoalTitle:
    value: str

    def __post_init__(self) -> None:
        if not self.value.strip():
            raise GoalValidationError("Goal title must not be empty")
        if len(self.value) > TITLE_MAX_LENGTH:
            raise GoalValidationError(
                f"Goal title must not exceed {TITLE_MAX_LENGTH} characters"
            )
