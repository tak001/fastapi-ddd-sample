from __future__ import annotations

from dataclasses import dataclass, replace

from domain.goal.exceptions import GoalValidationError
from domain.goal.value_objects import GoalId, GoalStatus, GoalTitle
from domain.task.value_objects import TaskId


@dataclass(frozen=True)
class Goal:
    """Goal aggregate root."""

    id: GoalId
    title: GoalTitle
    description: str
    status: GoalStatus
    task_ids: tuple[TaskId, ...]

    @classmethod
    def create(cls, title: str, description: str) -> Goal:
        return cls(
            id=GoalId.generate(),
            title=GoalTitle(value=title),
            description=description,
            status=GoalStatus.ACTIVE,
            task_ids=(),
        )

    def add_task_id(self, task_id: TaskId) -> Goal:
        if self.status != GoalStatus.ACTIVE:
            raise GoalValidationError(
                f"Cannot add tasks to a {self.status.value} goal"
            )
        return replace(self, task_ids=(*self.task_ids, task_id))

    def remove_task_id(self, task_id: TaskId) -> Goal:
        filtered = tuple(tid for tid in self.task_ids if tid != task_id)
        return replace(self, task_ids=filtered)

    def achieve(self) -> Goal:
        return replace(self, status=GoalStatus.ACHIEVED)

    def abandon(self) -> Goal:
        return replace(self, status=GoalStatus.ABANDONED)
