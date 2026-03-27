from dataclasses import dataclass

from application.shared.use_case import UseCase
from domain.task.exceptions import TaskNotFoundError
from domain.task.repository import TaskRepository
from domain.task.value_objects import TaskId


@dataclass(frozen=True)
class GetTaskQuery:
    task_id: str


@dataclass(frozen=True)
class GetTaskResult:
    id: str
    title: str
    description: str
    status: str
    priority: str
    goal_id: str | None
    due_date: str | None


class GetTaskUseCase(UseCase[GetTaskQuery, GetTaskResult]):
    def __init__(self, task_repository: TaskRepository) -> None:
        self._task_repository = task_repository

    def execute(self, input_data: GetTaskQuery) -> GetTaskResult:
        task = self._task_repository.find_by_id(TaskId(value=input_data.task_id))
        if task is None:
            raise TaskNotFoundError(input_data.task_id)
        return GetTaskResult(
            id=task.id.value,
            title=task.title.value,
            description=task.description,
            status=task.status.value,
            priority=task.priority.value,
            goal_id=task.goal_id.value if task.goal_id else None,
            due_date=task.due_date.value if task.due_date else None,
        )
