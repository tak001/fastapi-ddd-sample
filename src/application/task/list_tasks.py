from dataclasses import dataclass

from application.shared.use_case import UseCase
from domain.task.repository import TaskRepository


@dataclass(frozen=True)
class ListTasksQuery:
    pass


@dataclass(frozen=True)
class TaskItem:
    id: str
    title: str
    description: str
    status: str
    priority: str
    goal_id: str | None
    due_date: str | None


@dataclass(frozen=True)
class ListTasksResult:
    tasks: list[TaskItem]


class ListTasksUseCase(UseCase[ListTasksQuery, ListTasksResult]):
    def __init__(self, task_repository: TaskRepository) -> None:
        self._task_repository = task_repository

    def execute(self, input_data: ListTasksQuery) -> ListTasksResult:
        tasks = self._task_repository.find_all()
        return ListTasksResult(
            tasks=[
                TaskItem(
                    id=task.id.value,
                    title=task.title.value,
                    description=task.description,
                    status=task.status.value,
                    priority=task.priority.value,
                    goal_id=task.goal_id.value if task.goal_id else None,
                    due_date=task.due_date.value if task.due_date else None,
                )
                for task in tasks
            ]
        )
