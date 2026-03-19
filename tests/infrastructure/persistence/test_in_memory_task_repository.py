from domain.task.entity import Task
from domain.task.value_objects import TaskId
from infrastructure.persistence.in_memory_task_repository import InMemoryTaskRepository


class TestInMemoryTaskRepository:
    def test_save_and_find_by_id(self) -> None:
        repo = InMemoryTaskRepository()
        task = Task.create(title="Test", description="Desc")

        repo.save(task)
        found = repo.find_by_id(task.id)

        assert found is not None
        assert found.id == task.id
        assert found.title.value == "Test"

    def test_find_by_id_returns_none_for_unknown_id(self) -> None:
        repo = InMemoryTaskRepository()

        found = repo.find_by_id(TaskId(value="unknown"))

        assert found is None

    def test_find_all_empty(self) -> None:
        repo = InMemoryTaskRepository()

        result = repo.find_all()

        assert result == []

    def test_find_all_returns_all_saved_tasks(self) -> None:
        repo = InMemoryTaskRepository()
        task1 = Task.create(title="Task 1", description="")
        task2 = Task.create(title="Task 2", description="")
        repo.save(task1)
        repo.save(task2)

        result = repo.find_all()

        assert len(result) == 2

    def test_save_overwrites_existing_task(self) -> None:
        repo = InMemoryTaskRepository()
        task = Task.create(title="Original", description="")
        repo.save(task)

        updated = task.update_title("Updated")
        repo.save(updated)

        found = repo.find_by_id(task.id)
        assert found is not None
        assert found.title.value == "Updated"
        assert len(repo.find_all()) == 1
