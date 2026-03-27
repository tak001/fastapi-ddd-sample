from application.task.list_tasks_by_goal import ListTasksByGoalQuery, ListTasksByGoalUseCase
from domain.goal.value_objects import GoalId
from domain.task.entity import Task
from infrastructure.persistence.in_memory_task_repository import InMemoryTaskRepository


class TestListTasksByGoalUseCase:
    def test_list_tasks_returns_empty_when_no_tasks(self) -> None:
        repo = InMemoryTaskRepository()
        use_case = ListTasksByGoalUseCase(repo)
        goal_id = GoalId.generate()
        result = use_case.execute(ListTasksByGoalQuery(goal_id=goal_id.value))
        assert result.tasks == []

    def test_list_tasks_returns_only_matching_goal_tasks(self) -> None:
        repo = InMemoryTaskRepository()
        goal_id = GoalId.generate()
        other_goal_id = GoalId.generate()
        task1 = Task.create(title="Task 1", description="", goal_id=goal_id)
        task2 = Task.create(title="Task 2", description="", goal_id=goal_id)
        task3 = Task.create(title="Task 3", description="", goal_id=other_goal_id)
        repo.save(task1)
        repo.save(task2)
        repo.save(task3)
        use_case = ListTasksByGoalUseCase(repo)
        result = use_case.execute(ListTasksByGoalQuery(goal_id=goal_id.value))
        assert len(result.tasks) == 2
        task_titles = {t.title for t in result.tasks}
        assert task_titles == {"Task 1", "Task 2"}
