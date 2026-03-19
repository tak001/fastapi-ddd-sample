import pytest

from domain.task.entity import Task
from domain.task.repository import TaskRepository
from domain.task.value_objects import TaskId
from infrastructure.persistence.in_memory_task_repository import InMemoryTaskRepository


@pytest.fixture
def task_repository() -> TaskRepository:
    return InMemoryTaskRepository()


@pytest.fixture
def sample_task() -> Task:
    return Task.create(title="Sample task", description="A sample description")
