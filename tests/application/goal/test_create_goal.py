import pytest

from application.goal.create_goal import CreateGoalCommand, CreateGoalUseCase
from domain.goal.exceptions import GoalValidationError
from infrastructure.persistence.in_memory_goal_repository import InMemoryGoalRepository


class TestCreateGoalUseCase:
    def test_create_goal_returns_result(self) -> None:
        repo = InMemoryGoalRepository()
        use_case = CreateGoalUseCase(repo)
        result = use_case.execute(CreateGoalCommand(title="Learn Python", description="Master it"))
        assert result.title == "Learn Python"
        assert result.description == "Master it"
        assert result.status == "active"
        assert result.id != ""

    def test_create_goal_persists_to_repository(self) -> None:
        repo = InMemoryGoalRepository()
        use_case = CreateGoalUseCase(repo)
        result = use_case.execute(CreateGoalCommand(title="Test", description=""))
        goals = repo.find_all()
        assert len(goals) == 1
        assert goals[0].id.value == result.id

    def test_create_goal_with_invalid_title_raises_error(self) -> None:
        repo = InMemoryGoalRepository()
        use_case = CreateGoalUseCase(repo)
        with pytest.raises(GoalValidationError):
            use_case.execute(CreateGoalCommand(title="", description=""))
