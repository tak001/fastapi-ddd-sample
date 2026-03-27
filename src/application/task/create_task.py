from dataclasses import dataclass

from application.shared.use_case import UseCase
from domain.goal.value_objects import GoalId
from domain.task.entity import Task
from domain.task.repository import TaskRepository
from domain.task.exceptions import TaskValidationError
from domain.task.value_objects import TaskPriority


@dataclass(frozen=True)
class CreateTaskCommand:
    title: str
    description: str
    goal_id: str | None = None
    priority: str = "medium"
    due_date: str | None = None


@dataclass(frozen=True)
class CreateTaskResult:
    id: str
    title: str
    description: str
    status: str
    priority: str
    goal_id: str | None
    due_date: str | None


class CreateTaskUseCase(UseCase[CreateTaskCommand, CreateTaskResult]):
    def __init__(self, task_repository: TaskRepository) -> None:
        self._task_repository = task_repository

    def execute(self, input_data: CreateTaskCommand) -> CreateTaskResult:
        goal_id = GoalId(value=input_data.goal_id) if input_data.goal_id else None
        try:
            priority = TaskPriority(input_data.priority)
        except ValueError:
            raise TaskValidationError(f"Invalid priority: {input_data.priority}")
        task = Task.create(
            title=input_data.title,
            description=input_data.description,
            priority=priority,
            goal_id=goal_id,
            due_date=input_data.due_date,
        )
        self._task_repository.save(task)
        return CreateTaskResult(
            id=task.id.value,
            title=task.title.value,
            description=task.description,
            status=task.status.value,
            priority=task.priority.value,
            goal_id=task.goal_id.value if task.goal_id else None,
            due_date=task.due_date.value if task.due_date else None,
        )
