from abc import ABC, abstractmethod

from domain.task.entity import Task
from domain.task.value_objects import TaskId


class TaskRepository(ABC):
    """Driven port: persistence abstraction for Task aggregate."""

    @abstractmethod
    def save(self, task: Task) -> None: ...

    @abstractmethod
    def find_by_id(self, task_id: TaskId) -> Task | None: ...

    @abstractmethod
    def find_all(self) -> list[Task]: ...
