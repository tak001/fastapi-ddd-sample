from application.goal.list_goals import ListGoalsQuery, ListGoalsUseCase
from domain.goal.entity import Goal
from infrastructure.persistence.in_memory_goal_repository import InMemoryGoalRepository


class TestListGoalsUseCase:
    def test_list_goals_returns_empty_when_no_goals(self) -> None:
        repo = InMemoryGoalRepository()
        use_case = ListGoalsUseCase(repo)
        result = use_case.execute(ListGoalsQuery())
        assert result.goals == []

    def test_list_goals_returns_all_goals(self) -> None:
        repo = InMemoryGoalRepository()
        repo.save(Goal.create(title="Goal 1", description=""))
        repo.save(Goal.create(title="Goal 2", description=""))
        use_case = ListGoalsUseCase(repo)
        result = use_case.execute(ListGoalsQuery())
        assert len(result.goals) == 2
