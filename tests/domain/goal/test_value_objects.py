import pytest

from domain.goal.exceptions import GoalValidationError
from domain.goal.value_objects import GoalId, GoalStatus, GoalTitle


class TestGoalId:
    def test_generate_creates_unique_ids(self) -> None:
        id1 = GoalId.generate()
        id2 = GoalId.generate()
        assert id1 != id2

    def test_same_value_is_equal(self) -> None:
        id1 = GoalId(value="abc123")
        id2 = GoalId(value="abc123")
        assert id1 == id2

    def test_is_immutable(self) -> None:
        goal_id = GoalId(value="abc123")
        with pytest.raises(AttributeError):
            goal_id.value = "changed"  # type: ignore[misc]


class TestGoalStatus:
    def test_has_active_status(self) -> None:
        assert GoalStatus.ACTIVE.value == "active"

    def test_has_achieved_status(self) -> None:
        assert GoalStatus.ACHIEVED.value == "achieved"

    def test_has_abandoned_status(self) -> None:
        assert GoalStatus.ABANDONED.value == "abandoned"


class TestGoalTitle:
    def test_valid_title(self) -> None:
        title = GoalTitle(value="Learn Python")
        assert title.value == "Learn Python"

    def test_empty_title_raises_error(self) -> None:
        with pytest.raises(GoalValidationError, match="empty"):
            GoalTitle(value="")

    def test_whitespace_only_title_raises_error(self) -> None:
        with pytest.raises(GoalValidationError, match="empty"):
            GoalTitle(value="   ")

    def test_too_long_title_raises_error(self) -> None:
        with pytest.raises(GoalValidationError, match="200"):
            GoalTitle(value="a" * 201)

    def test_max_length_title_is_valid(self) -> None:
        title = GoalTitle(value="a" * 200)
        assert len(title.value) == 200

    def test_is_immutable(self) -> None:
        title = GoalTitle(value="Test")
        with pytest.raises(AttributeError):
            title.value = "Changed"  # type: ignore[misc]
