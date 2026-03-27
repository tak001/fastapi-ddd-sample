import pytest

from application.goal.add_task_to_goal import AddTaskToGoalCommand, AddTaskToGoalUseCase
from application.goal.create_goal import CreateGoalCommand, CreateGoalUseCase
from application.task.create_task import CreateTaskCommand, CreateTaskUseCase
from domain.goal.exceptions import GoalNotFoundError
from infrastructure.persistence.in_memory_goal_repository import InMemoryGoalRepository
from infrastructure.persistence.in_memory_task_repository import InMemoryTaskRepository


class TestAddTaskToGoalUseCase:
    def test_adds_task_id_to_goal(self) -> None:
        goal_repo = InMemoryGoalRepository()
        task_repo = InMemoryTaskRepository()
        goal_result = CreateGoalUseCase(goal_repo).execute(
            CreateGoalCommand(title="My Goal", description="desc")
        )
        task_result = CreateTaskUseCase(task_repo).execute(
            CreateTaskCommand(title="Task A", description="do it")
        )

        use_case = AddTaskToGoalUseCase(goal_repo)
        result = use_case.execute(
            AddTaskToGoalCommand(goal_id=goal_result.id, task_id=task_result.id)
        )

        assert result.goal_id == goal_result.id
        assert result.task_id == task_result.id
        from domain.goal.value_objects import GoalId
        goal = goal_repo.find_by_id(GoalId(value=goal_result.id))
        assert goal is not None
        assert any(t.value == task_result.id for t in goal.task_ids)

    def test_raises_error_for_nonexistent_goal(self) -> None:
        goal_repo = InMemoryGoalRepository()
        use_case = AddTaskToGoalUseCase(goal_repo)

        with pytest.raises(GoalNotFoundError):
            use_case.execute(AddTaskToGoalCommand(goal_id="nonexistent", task_id="any"))
