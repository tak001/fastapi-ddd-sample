import pytest

from application.task.create_task import CreateTaskCommand, CreateTaskUseCase
from domain.task.exceptions import TaskValidationError
from domain.task.repository import TaskRepository


class TestCreateTaskUseCase:
    def test_create_task_successfully(self, task_repository: TaskRepository) -> None:
        use_case = CreateTaskUseCase(task_repository)
        command = CreateTaskCommand(title="Buy groceries", description="Milk and eggs")

        result = use_case.execute(command)

        assert result.title == "Buy groceries"
        assert result.description == "Milk and eggs"
        assert result.status == "todo"
        assert result.id != ""

    def test_created_task_is_persisted(self, task_repository: TaskRepository) -> None:
        use_case = CreateTaskUseCase(task_repository)
        command = CreateTaskCommand(title="Persisted task", description="")

        result = use_case.execute(command)
        found = task_repository.find_all()

        assert len(found) == 1
        assert found[0].id.value == result.id

    def test_create_task_with_invalid_title_raises_error(
        self, task_repository: TaskRepository
    ) -> None:
        use_case = CreateTaskUseCase(task_repository)
        command = CreateTaskCommand(title="", description="")

        with pytest.raises(TaskValidationError):
            use_case.execute(command)
