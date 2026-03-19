"""Composition Root: wires all dependencies together."""

from application.task.create_task import CreateTaskUseCase
from application.task.get_task import GetTaskUseCase
from application.task.list_tasks import ListTasksUseCase
from infrastructure.persistence.in_memory_task_repository import InMemoryTaskRepository

_task_repository = InMemoryTaskRepository()

_create_task_use_case = CreateTaskUseCase(_task_repository)
_get_task_use_case = GetTaskUseCase(_task_repository)
_list_tasks_use_case = ListTasksUseCase(_task_repository)


def get_create_task_use_case() -> CreateTaskUseCase:
    return _create_task_use_case


def get_get_task_use_case() -> GetTaskUseCase:
    return _get_task_use_case


def get_list_tasks_use_case() -> ListTasksUseCase:
    return _list_tasks_use_case
