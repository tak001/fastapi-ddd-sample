from abc import ABC, abstractmethod

from domain.goal.entity import Goal
from domain.goal.value_objects import GoalId


class GoalRepository(ABC):
    """Driven port: persistence abstraction for Goal aggregate."""

    @abstractmethod
    def save(self, goal: Goal) -> None: ...

    @abstractmethod
    def find_by_id(self, goal_id: GoalId) -> Goal | None: ...

    @abstractmethod
    def find_all(self) -> list[Goal]: ...
