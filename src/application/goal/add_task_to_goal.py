from dataclasses import dataclass

from application.shared.use_case import UseCase
from domain.goal.exceptions import GoalNotFoundError
from domain.goal.repository import GoalRepository
from domain.goal.value_objects import GoalId
from domain.task.value_objects import TaskId


@dataclass(frozen=True)
class AddTaskToGoalCommand:
    goal_id: str
    task_id: str


@dataclass(frozen=True)
class AddTaskToGoalResult:
    goal_id: str
    task_id: str


class AddTaskToGoalUseCase(UseCase[AddTaskToGoalCommand, AddTaskToGoalResult]):
    def __init__(self, goal_repository: GoalRepository) -> None:
        self._goal_repository = goal_repository

    def execute(self, input_data: AddTaskToGoalCommand) -> AddTaskToGoalResult:
        goal = self._goal_repository.find_by_id(GoalId(value=input_data.goal_id))
        if goal is None:
            raise GoalNotFoundError(input_data.goal_id)
        updated_goal = goal.add_task_id(TaskId(value=input_data.task_id))
        self._goal_repository.save(updated_goal)
        return AddTaskToGoalResult(goal_id=input_data.goal_id, task_id=input_data.task_id)
