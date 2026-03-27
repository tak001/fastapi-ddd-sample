from domain.goal.value_objects import GoalId
from domain.task.entity import Task
from domain.task.repository import TaskRepository
from domain.task.value_objects import TaskId


class InMemoryTaskRepository(TaskRepository):
    def __init__(self) -> None:
        self._storage: dict[str, Task] = {}

    def save(self, task: Task) -> None:
        self._storage[task.id.value] = task

    def find_by_id(self, task_id: TaskId) -> Task | None:
        return self._storage.get(task_id.value)

    def find_all(self) -> list[Task]:
        return list(self._storage.values())

    def find_by_goal_id(self, goal_id: GoalId) -> list[Task]:
        return [
            task for task in self._storage.values()
            if task.goal_id is not None and task.goal_id == goal_id
        ]
