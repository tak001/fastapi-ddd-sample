from abc import ABC, abstractmethod
from typing import Generic, TypeVar

TInput = TypeVar("TInput")
TOutput = TypeVar("TOutput")


class UseCase(ABC, Generic[TInput, TOutput]):
    """Driver port: defines the contract for application use cases."""

    @abstractmethod
    def execute(self, input_data: TInput) -> TOutput: ...
