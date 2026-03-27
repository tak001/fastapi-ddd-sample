from domain.goal.entity import Goal
from domain.goal.value_objects import GoalId
from infrastructure.persistence.in_memory_goal_repository import InMemoryGoalRepository


class TestInMemoryGoalRepository:
    def test_save_and_find_by_id(self) -> None:
        repo = InMemoryGoalRepository()
        goal = Goal.create(title="Test", description="Desc")
        repo.save(goal)
        found = repo.find_by_id(goal.id)
        assert found is not None
        assert found.id == goal.id

    def test_find_by_id_returns_none_when_not_found(self) -> None:
        repo = InMemoryGoalRepository()
        found = repo.find_by_id(GoalId(value="nonexistent"))
        assert found is None

    def test_find_all_returns_empty_list(self) -> None:
        repo = InMemoryGoalRepository()
        assert repo.find_all() == []

    def test_find_all_returns_all_goals(self) -> None:
        repo = InMemoryGoalRepository()
        repo.save(Goal.create(title="Goal 1", description=""))
        repo.save(Goal.create(title="Goal 2", description=""))
        assert len(repo.find_all()) == 2

    def test_save_overwrites_existing(self) -> None:
        repo = InMemoryGoalRepository()
        goal = Goal.create(title="Original", description="")
        repo.save(goal)
        updated = goal.achieve()
        repo.save(updated)
        found = repo.find_by_id(goal.id)
        assert found is not None
        assert found.status.value == "achieved"
