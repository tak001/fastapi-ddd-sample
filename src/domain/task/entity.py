from __future__ import annotations

from dataclasses import dataclass, replace

from domain.task.value_objects import TaskId, TaskStatus, TaskTitle


@dataclass(frozen=True)
class Task:
    """Task aggregate root."""

    id: TaskId
    title: TaskTitle
    description: str
    status: TaskStatus

    @classmethod
    def create(cls, title: str, description: str) -> Task:
        return cls(
            id=TaskId.generate(),
            title=TaskTitle(value=title),
            description=description,
            status=TaskStatus.TODO,
        )

    def change_status(self, new_status: TaskStatus) -> Task:
        return replace(self, status=new_status)

    def update_title(self, new_title: str) -> Task:
        return replace(self, title=TaskTitle(value=new_title))
