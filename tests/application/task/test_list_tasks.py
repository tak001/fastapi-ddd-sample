from application.task.list_tasks import ListTasksQuery, ListTasksUseCase
from domain.task.entity import Task
from domain.task.repository import TaskRepository


class TestListTasksUseCase:
    def test_list_empty(self, task_repository: TaskRepository) -> None:
        use_case = ListTasksUseCase(task_repository)

        result = use_case.execute(ListTasksQuery())

        assert result.tasks == []

    def test_list_multiple_tasks(self, task_repository: TaskRepository) -> None:
        task1 = Task.create(title="Task 1", description="First")
        task2 = Task.create(title="Task 2", description="Second")
        task_repository.save(task1)
        task_repository.save(task2)

        use_case = ListTasksUseCase(task_repository)
        result = use_case.execute(ListTasksQuery())

        assert len(result.tasks) == 2
        titles = {t.title for t in result.tasks}
        assert titles == {"Task 1", "Task 2"}
