from dataclasses import dataclass

from application.shared.use_case import UseCase
from domain.goal.exceptions import GoalNotFoundError
from domain.goal.repository import GoalRepository
from domain.goal.value_objects import GoalId


@dataclass(frozen=True)
class GetGoalQuery:
    goal_id: str


@dataclass(frozen=True)
class GetGoalResult:
    id: str
    title: str
    description: str
    status: str
    task_ids: list[str]


class GetGoalUseCase(UseCase[GetGoalQuery, GetGoalResult]):
    def __init__(self, goal_repository: GoalRepository) -> None:
        self._goal_repository = goal_repository

    def execute(self, input_data: GetGoalQuery) -> GetGoalResult:
        goal = self._goal_repository.find_by_id(GoalId(value=input_data.goal_id))
        if goal is None:
            raise GoalNotFoundError(input_data.goal_id)
        return GetGoalResult(
            id=goal.id.value,
            title=goal.title.value,
            description=goal.description,
            status=goal.status.value,
            task_ids=[tid.value for tid in goal.task_ids],
        )
