import pytest

from domain.goal.value_objects import GoalId
from domain.task.entity import Task
from domain.task.exceptions import TaskValidationError
from domain.task.value_objects import TaskPriority, TaskStatus


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


class TestTaskCreateWithExtendedFields:
    def test_create_task_default_priority_is_medium(self) -> None:
        task = Task.create(title="Test", description="")
        assert task.priority == TaskPriority.MEDIUM

    def test_create_task_default_goal_id_is_none(self) -> None:
        task = Task.create(title="Test", description="")
        assert task.goal_id is None

    def test_create_task_default_due_date_is_none(self) -> None:
        task = Task.create(title="Test", description="")
        assert task.due_date is None

    def test_create_task_with_priority(self) -> None:
        task = Task.create(title="Test", description="", priority=TaskPriority.HIGH)
        assert task.priority == TaskPriority.HIGH

    def test_create_task_with_goal_id(self) -> None:
        goal_id = GoalId.generate()
        task = Task.create(title="Test", description="", goal_id=goal_id)
        assert task.goal_id == goal_id

    def test_create_task_with_due_date(self) -> None:
        task = Task.create(title="Test", description="", due_date="2026-04-01")
        assert task.due_date is not None
        assert task.due_date.value == "2026-04-01"


class TestTaskAssignToGoal:
    def test_assign_to_goal(self) -> None:
        task = Task.create(title="Test", description="")
        goal_id = GoalId.generate()
        updated = task.assign_to_goal(goal_id)
        assert updated.goal_id == goal_id

    def test_assign_to_goal_returns_new_instance(self) -> None:
        task = Task.create(title="Test", description="")
        goal_id = GoalId.generate()
        updated = task.assign_to_goal(goal_id)
        assert task is not updated
        assert task.goal_id is None


class TestTaskSetPriority:
    def test_set_priority(self) -> None:
        task = Task.create(title="Test", description="")
        updated = task.set_priority(TaskPriority.HIGH)
        assert updated.priority == TaskPriority.HIGH

    def test_set_priority_returns_new_instance(self) -> None:
        task = Task.create(title="Test", description="")
        updated = task.set_priority(TaskPriority.LOW)
        assert task is not updated
        assert task.priority == TaskPriority.MEDIUM


class TestTaskSetDueDate:
    def test_set_due_date(self) -> None:
        task = Task.create(title="Test", description="")
        updated = task.set_due_date("2026-05-01")
        assert updated.due_date is not None
        assert updated.due_date.value == "2026-05-01"

    def test_set_due_date_with_invalid_format_raises_error(self) -> None:
        task = Task.create(title="Test", description="")
        with pytest.raises(Exception, match="YYYY-MM-DD"):
            task.set_due_date("invalid")


class TestTaskImmutability:
    def test_task_is_immutable(self) -> None:
        task = Task.create(title="Test", description="")
        with pytest.raises(AttributeError):
            task.description = "Changed"  # type: ignore[misc]
