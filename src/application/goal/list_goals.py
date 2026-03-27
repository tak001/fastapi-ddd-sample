from dataclasses import dataclass

from application.shared.use_case import UseCase
from domain.goal.repository import GoalRepository


@dataclass(frozen=True)
class ListGoalsQuery:
    pass


@dataclass(frozen=True)
class GoalItem:
    id: str
    title: str
    description: str
    status: str


@dataclass(frozen=True)
class ListGoalsResult:
    goals: list[GoalItem]


class ListGoalsUseCase(UseCase[ListGoalsQuery, ListGoalsResult]):
    def __init__(self, goal_repository: GoalRepository) -> None:
        self._goal_repository = goal_repository

    def execute(self, input_data: ListGoalsQuery) -> ListGoalsResult:
        goals = self._goal_repository.find_all()
        return ListGoalsResult(
            goals=[
                GoalItem(
                    id=goal.id.value,
                    title=goal.title.value,
                    description=goal.description,
                    status=goal.status.value,
                )
                for goal in goals
            ]
        )
