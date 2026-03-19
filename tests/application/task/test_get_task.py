import pytest

from application.task.get_task import GetTaskQuery, GetTaskUseCase
from domain.task.entity import Task
from domain.task.exceptions import TaskNotFoundError
from domain.task.repository import TaskRepository


class TestGetTaskUseCase:
    def test_get_existing_task(
        self, task_repository: TaskRepository, sample_task: Task
    ) -> None:
        task_repository.save(sample_task)
        use_case = GetTaskUseCase(task_repository)
        query = GetTaskQuery(task_id=sample_task.id.value)

        result = use_case.execute(query)

        assert result.id == sample_task.id.value
        assert result.title == sample_task.title.value
        assert result.description == sample_task.description

    def test_get_nonexistent_task_raises_error(
        self, task_repository: TaskRepository
    ) -> None:
        use_case = GetTaskUseCase(task_repository)
        query = GetTaskQuery(task_id="nonexistent-id")

        with pytest.raises(TaskNotFoundError):
            use_case.execute(query)
