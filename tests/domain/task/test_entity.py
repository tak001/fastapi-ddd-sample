import pytest

from domain.task.entity import Task
from domain.task.value_objects import TaskStatus
from domain.task.exceptions import TaskValidationError


class TestTaskCreate:
    def test_create_task_with_valid_data(self) -> None:
        task = Task.create(title="Buy groceries", description="Milk and eggs")
        assert task.title.value == "Buy groceries"
        assert task.description == "Milk and eggs"
        assert task.status == TaskStatus.TODO

    def test_create_task_generates_unique_id(self) -> None:
        task1 = Task.create(title="Task 1", description="")
        task2 = Task.create(title="Task 2", description="")
        assert task1.id != task2.id

    def test_create_task_with_empty_description(self) -> None:
        task = Task.create(title="Test", description="")
        assert task.description == ""

    def test_create_task_with_invalid_title_raises_error(self) -> None:
        with pytest.raises(TaskValidationError):
            Task.create(title="", description="")


class TestTaskChangeStatus:
    def test_change_status_to_in_progress(self) -> None:
        task = Task.create(title="Test", description="")
        updated = task.change_status(TaskStatus.IN_PROGRESS)
        assert updated.status == TaskStatus.IN_PROGRESS

    def test_change_status_returns_new_instance(self) -> None:
        task = Task.create(title="Test", description="")
        updated = task.change_status(TaskStatus.IN_PROGRESS)
        assert task is not updated
        assert task.status == TaskStatus.TODO

    def test_change_status_preserves_other_fields(self) -> None:
        task = Task.create(title="Test", description="Desc")
        updated = task.change_status(TaskStatus.DONE)
        assert updated.id == task.id
        assert updated.title == task.title
        assert updated.description == task.description


class TestTaskUpdateTitle:
    def test_update_title(self) -> None:
        task = Task.create(title="Old title", description="")
        updated = task.update_title("New title")
        assert updated.title.value == "New title"

    def test_update_title_returns_new_instance(self) -> None:
        task = Task.create(title="Old", description="")
        updated = task.update_title("New")
        assert task is not updated
        assert task.title.value == "Old"

    def test_update_title_with_invalid_title_raises_error(self) -> None:
        task = Task.create(title="Valid", description="")
        with pytest.raises(TaskValidationError):
            task.update_title("")


class TestTaskImmutability:
    def test_task_is_immutable(self) -> None:
        task = Task.create(title="Test", description="")
        with pytest.raises(AttributeError):
            task.description = "Changed"  # type: ignore[misc]
