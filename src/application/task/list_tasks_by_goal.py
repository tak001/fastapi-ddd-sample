from dataclasses import dataclass

from application.shared.use_case import UseCase
from domain.goal.value_objects import GoalId
from domain.task.repository import TaskRepository


@dataclass(frozen=True)
class ListTasksByGoalQuery:
    goal_id: str


@dataclass(frozen=True)
class TaskByGoalItem:
    id: str
    title: str
    description: str
    status: str
    priority: str
    due_date: str | None


@dataclass(frozen=True)
class ListTasksByGoalResult:
    tasks: list[TaskByGoalItem]


class ListTasksByGoalUseCase(UseCase[ListTasksByGoalQuery, ListTasksByGoalResult]):
    def __init__(self, task_repository: TaskRepository) -> None:
        self._task_repository = task_repository

    def execute(self, input_data: ListTasksByGoalQuery) -> ListTasksByGoalResult:
        goal_id = GoalId(value=input_data.goal_id)
        tasks = self._task_repository.find_by_goal_id(goal_id)
        return ListTasksByGoalResult(
            tasks=[
                TaskByGoalItem(
                    id=task.id.value,
                    title=task.title.value,
                    description=task.description,
                    status=task.status.value,
                    priority=task.priority.value,
                    due_date=task.due_date.value if task.due_date else None,
                )
                for task in tasks
            ]
        )
