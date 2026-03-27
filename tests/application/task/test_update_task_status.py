import pytest

from application.task.update_task_status import UpdateTaskStatusCommand, UpdateTaskStatusUseCase
from domain.task.entity import Task
from domain.task.exceptions import TaskNotFoundError
from infrastructure.persistence.in_memory_task_repository import InMemoryTaskRepository


class TestUpdateTaskStatusUseCase:
    def test_update_status_to_in_progress(self) -> None:
        repo = InMemoryTaskRepository()
        task = Task.create(title="Test", description="")
        repo.save(task)
        use_case = UpdateTaskStatusUseCase(repo)
        result = use_case.execute(
            UpdateTaskStatusCommand(task_id=task.id.value, status="in_progress")
        )
        assert result.status == "in_progress"

    def test_update_status_persists_change(self) -> None:
        repo = InMemoryTaskRepository()
        task = Task.create(title="Test", description="")
        repo.save(task)
        use_case = UpdateTaskStatusUseCase(repo)
        use_case.execute(UpdateTaskStatusCommand(task_id=task.id.value, status="done"))
        saved = repo.find_by_id(task.id)
        assert saved is not None
        assert saved.status.value == "done"

    def test_update_nonexistent_task_raises_error(self) -> None:
        repo = InMemoryTaskRepository()
        use_case = UpdateTaskStatusUseCase(repo)
        with pytest.raises(TaskNotFoundError):
            use_case.execute(UpdateTaskStatusCommand(task_id="nonexistent", status="done"))
