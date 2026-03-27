import pytest

from application.goal.get_goal import GetGoalQuery, GetGoalUseCase
from domain.goal.entity import Goal
from domain.goal.exceptions import GoalNotFoundError
from infrastructure.persistence.in_memory_goal_repository import InMemoryGoalRepository


class TestGetGoalUseCase:
    def test_get_existing_goal(self) -> None:
        repo = InMemoryGoalRepository()
        goal = Goal.create(title="Test", description="Desc")
        repo.save(goal)
        use_case = GetGoalUseCase(repo)
        result = use_case.execute(GetGoalQuery(goal_id=goal.id.value))
        assert result.id == goal.id.value
        assert result.title == "Test"
        assert result.description == "Desc"
        assert result.status == "active"
        assert result.task_ids == []

    def test_get_nonexistent_goal_raises_error(self) -> None:
        repo = InMemoryGoalRepository()
        use_case = GetGoalUseCase(repo)
        with pytest.raises(GoalNotFoundError):
            use_case.execute(GetGoalQuery(goal_id="nonexistent"))
