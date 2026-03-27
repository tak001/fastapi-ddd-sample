import pytest

from domain.task.exceptions import TaskValidationError
from domain.task.value_objects import TaskDueDate, TaskId, TaskPriority, TaskStatus, TaskTitle


class TestTaskId:
    def test_generate_creates_unique_ids(self) -> None:
        id1 = TaskId.generate()
        id2 = TaskId.generate()
        assert id1 != id2

    def test_same_value_is_equal(self) -> None:
        id1 = TaskId(value="abc123")
        id2 = TaskId(value="abc123")
        assert id1 == id2

    def test_different_value_is_not_equal(self) -> None:
        id1 = TaskId(value="abc")
        id2 = TaskId(value="xyz")
        assert id1 != id2

    def test_is_hashable(self) -> None:
        task_id = TaskId(value="abc123")
        assert hash(task_id) == hash(TaskId(value="abc123"))

    def test_is_immutable(self) -> None:
        task_id = TaskId(value="abc123")
        with pytest.raises(AttributeError):
            task_id.value = "changed"  # type: ignore[misc]


class TestTaskStatus:
    def test_has_todo_status(self) -> None:
        assert TaskStatus.TODO.value == "todo"

    def test_has_in_progress_status(self) -> None:
        assert TaskStatus.IN_PROGRESS.value == "in_progress"

    def test_has_done_status(self) -> None:
        assert TaskStatus.DONE.value == "done"


class TestTaskTitle:
    def test_valid_title(self) -> None:
        title = TaskTitle(value="Buy groceries")
        assert title.value == "Buy groceries"

    def test_empty_title_raises_error(self) -> None:
        with pytest.raises(TaskValidationError, match="empty"):
            TaskTitle(value="")

    def test_whitespace_only_title_raises_error(self) -> None:
        with pytest.raises(TaskValidationError, match="empty"):
            TaskTitle(value="   ")

    def test_too_long_title_raises_error(self) -> None:
        with pytest.raises(TaskValidationError, match="100"):
            TaskTitle(value="a" * 101)

    def test_max_length_title_is_valid(self) -> None:
        title = TaskTitle(value="a" * 100)
        assert len(title.value) == 100

    def test_is_immutable(self) -> None:
        title = TaskTitle(value="Test")
        with pytest.raises(AttributeError):
            title.value = "Changed"  # type: ignore[misc]


class TestTaskPriority:
    def test_has_high_priority(self) -> None:
        assert TaskPriority.HIGH.value == "high"

    def test_has_medium_priority(self) -> None:
        assert TaskPriority.MEDIUM.value == "medium"

    def test_has_low_priority(self) -> None:
        assert TaskPriority.LOW.value == "low"


class TestTaskDueDate:
    def test_valid_date(self) -> None:
        due_date = TaskDueDate(value="2026-04-01")
        assert due_date.value == "2026-04-01"

    def test_invalid_format_raises_error(self) -> None:
        with pytest.raises(TaskValidationError, match="YYYY-MM-DD"):
            TaskDueDate(value="2026/04/01")

    def test_empty_string_raises_error(self) -> None:
        with pytest.raises(TaskValidationError, match="YYYY-MM-DD"):
            TaskDueDate(value="")

    def test_partial_date_raises_error(self) -> None:
        with pytest.raises(TaskValidationError, match="YYYY-MM-DD"):
            TaskDueDate(value="2026-04")

    def test_is_immutable(self) -> None:
        due_date = TaskDueDate(value="2026-04-01")
        with pytest.raises(AttributeError):
            due_date.value = "2026-05-01"  # type: ignore[misc]
