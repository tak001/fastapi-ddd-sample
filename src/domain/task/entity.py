from __future__ import annotations

from dataclasses import dataclass, replace

from domain.goal.value_objects import GoalId
from domain.task.value_objects import TaskDueDate, TaskId, TaskPriority, TaskStatus, TaskTitle


@dataclass(frozen=True)
class Task:
    """Task aggregate root."""

    id: TaskId
    title: TaskTitle
    description: str
    status: TaskStatus
    priority: TaskPriority
    goal_id: GoalId | None
    due_date: TaskDueDate | None

    @classmethod
    def create(
        cls,
        title: str,
        description: str,
        priority: TaskPriority = TaskPriority.MEDIUM,
        goal_id: GoalId | None = None,
        due_date: str | None = None,
    ) -> Task:
        return cls(
            id=TaskId.generate(),
            title=TaskTitle(value=title),
            description=description,
            status=TaskStatus.TODO,
            priority=priority,
            goal_id=goal_id,
            due_date=TaskDueDate(value=due_date) if due_date else None,
        )

    def change_status(self, new_status: TaskStatus) -> Task:
        return replace(self, status=new_status)

    def update_title(self, new_title: str) -> Task:
        return replace(self, title=TaskTitle(value=new_title))

    def assign_to_goal(self, goal_id: GoalId) -> Task:
        return replace(self, goal_id=goal_id)

    def set_priority(self, priority: TaskPriority) -> Task:
        return replace(self, priority=priority)

    def set_due_date(self, due_date: str) -> Task:
        return replace(self, due_date=TaskDueDate(value=due_date))
