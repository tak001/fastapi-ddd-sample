import pytest

from domain.goal.entity import Goal
from domain.goal.exceptions import GoalValidationError
from domain.goal.value_objects import GoalStatus
from domain.task.value_objects import TaskId


class TestGoalCreate:
    def test_create_goal_with_valid_data(self) -> None:
        goal = Goal.create(title="Learn Python", description="Master Python programming")
        assert goal.title.value == "Learn Python"
        assert goal.description == "Master Python programming"
        assert goal.status == GoalStatus.ACTIVE
        assert goal.task_ids == ()

    def test_create_goal_generates_unique_id(self) -> None:
        goal1 = Goal.create(title="Goal 1", description="")
        goal2 = Goal.create(title="Goal 2", description="")
        assert goal1.id != goal2.id

    def test_create_goal_with_empty_description(self) -> None:
        goal = Goal.create(title="Test", description="")
        assert goal.description == ""

    def test_create_goal_with_invalid_title_raises_error(self) -> None:
        with pytest.raises(GoalValidationError):
            Goal.create(title="", description="")


class TestGoalAddTaskId:
    def test_add_task_id_to_active_goal(self) -> None:
        goal = Goal.create(title="Test", description="")
        task_id = TaskId.generate()
        updated = goal.add_task_id(task_id)
        assert task_id in updated.task_ids
        assert len(updated.task_ids) == 1

    def test_add_task_id_returns_new_instance(self) -> None:
        goal = Goal.create(title="Test", description="")
        task_id = TaskId.generate()
        updated = goal.add_task_id(task_id)
        assert goal is not updated
        assert goal.task_ids == ()

    def test_add_multiple_task_ids_preserves_order(self) -> None:
        goal = Goal.create(title="Test", description="")
        id1 = TaskId.generate()
        id2 = TaskId.generate()
        updated = goal.add_task_id(id1).add_task_id(id2)
        assert updated.task_ids == (id1, id2)

    def test_add_task_id_to_achieved_goal_raises_error(self) -> None:
        goal = Goal.create(title="Test", description="").achieve()
        with pytest.raises(GoalValidationError, match="achieved"):
            goal.add_task_id(TaskId.generate())

    def test_add_task_id_to_abandoned_goal_raises_error(self) -> None:
        goal = Goal.create(title="Test", description="").abandon()
        with pytest.raises(GoalValidationError, match="abandoned"):
            goal.add_task_id(TaskId.generate())


class TestGoalRemoveTaskId:
    def test_remove_task_id(self) -> None:
        goal = Goal.create(title="Test", description="")
        task_id = TaskId.generate()
        goal_with_task = goal.add_task_id(task_id)
        updated = goal_with_task.remove_task_id(task_id)
        assert task_id not in updated.task_ids
        assert len(updated.task_ids) == 0

    def test_remove_nonexistent_task_id_returns_same_state(self) -> None:
        goal = Goal.create(title="Test", description="")
        updated = goal.remove_task_id(TaskId.generate())
        assert updated.task_ids == ()


class TestGoalStatusTransition:
    def test_achieve_goal(self) -> None:
        goal = Goal.create(title="Test", description="")
        updated = goal.achieve()
        assert updated.status == GoalStatus.ACHIEVED

    def test_abandon_goal(self) -> None:
        goal = Goal.create(title="Test", description="")
        updated = goal.abandon()
        assert updated.status == GoalStatus.ABANDONED

    def test_status_transition_returns_new_instance(self) -> None:
        goal = Goal.create(title="Test", description="")
        achieved = goal.achieve()
        assert goal is not achieved
        assert goal.status == GoalStatus.ACTIVE


class TestGoalImmutability:
    def test_goal_is_immutable(self) -> None:
        goal = Goal.create(title="Test", description="")
        with pytest.raises(AttributeError):
            goal.description = "Changed"  # type: ignore[misc]
