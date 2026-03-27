from dataclasses import dataclass

from application.shared.use_case import UseCase
from domain.goal.entity import Goal
from domain.goal.repository import GoalRepository


@dataclass(frozen=True)
class CreateGoalCommand:
    title: str
    description: str


@dataclass(frozen=True)
class CreateGoalResult:
    id: str
    title: str
    description: str
    status: str


class CreateGoalUseCase(UseCase[CreateGoalCommand, CreateGoalResult]):
    def __init__(self, goal_repository: GoalRepository) -> None:
        self._goal_repository = goal_repository

    def execute(self, input_data: CreateGoalCommand) -> CreateGoalResult:
        goal = Goal.create(
            title=input_data.title,
            description=input_data.description,
        )
        self._goal_repository.save(goal)
        return CreateGoalResult(
            id=goal.id.value,
            title=goal.title.value,
            description=goal.description,
            status=goal.status.value,
        )
