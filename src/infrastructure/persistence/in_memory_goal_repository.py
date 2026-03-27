from domain.goal.entity import Goal
from domain.goal.repository import GoalRepository
from domain.goal.value_objects import GoalId


class InMemoryGoalRepository(GoalRepository):
    def __init__(self) -> None:
        self._storage: dict[str, Goal] = {}

    def save(self, goal: Goal) -> None:
        self._storage[goal.id.value] = goal

    def find_by_id(self, goal_id: GoalId) -> Goal | None:
        return self._storage.get(goal_id.value)

    def find_all(self) -> list[Goal]:
        return list(self._storage.values())
