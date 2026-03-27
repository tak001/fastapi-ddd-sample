from dataclasses import dataclass

from application.shared.use_case import UseCase
from domain.task.exceptions import TaskNotFoundError
from domain.task.repository import TaskRepository
from domain.task.value_objects import TaskId, TaskStatus


@dataclass(frozen=True)
class UpdateTaskStatusCommand:
    task_id: str
    status: str


@dataclass(frozen=True)
class UpdateTaskStatusResult:
    id: str
    title: str
    description: str
    status: str


class UpdateTaskStatusUseCase(UseCase[UpdateTaskStatusCommand, UpdateTaskStatusResult]):
    def __init__(self, task_repository: TaskRepository) -> None:
        self._task_repository = task_repository

    def execute(self, input_data: UpdateTaskStatusCommand) -> UpdateTaskStatusResult:
        task = self._task_repository.find_by_id(TaskId(value=input_data.task_id))
        if task is None:
            raise TaskNotFoundError(input_data.task_id)
        new_status = TaskStatus(input_data.status)
        updated_task = task.change_status(new_status)
        self._task_repository.save(updated_task)
        return UpdateTaskStatusResult(
            id=updated_task.id.value,
            title=updated_task.title.value,
            description=updated_task.description,
            status=updated_task.status.value,
        )
