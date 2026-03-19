from dataclasses import dataclass

from application.shared.use_case import UseCase
from domain.task.entity import Task
from domain.task.repository import TaskRepository


@dataclass(frozen=True)
class CreateTaskCommand:
    title: str
    description: str


@dataclass(frozen=True)
class CreateTaskResult:
    id: str
    title: str
    description: str
    status: str


class CreateTaskUseCase(UseCase[CreateTaskCommand, CreateTaskResult]):
    def __init__(self, task_repository: TaskRepository) -> None:
        self._task_repository = task_repository

    def execute(self, input_data: CreateTaskCommand) -> CreateTaskResult:
        task = Task.create(
            title=input_data.title,
            description=input_data.description,
        )
        self._task_repository.save(task)
        return CreateTaskResult(
            id=task.id.value,
            title=task.title.value,
            description=task.description,
            status=task.status.value,
        )
