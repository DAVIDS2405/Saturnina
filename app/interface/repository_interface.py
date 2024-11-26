from abc import ABC, abstractmethod
from typing import Any, List


class RepositoryInterface(ABC):

    @abstractmethod
    def create(self, data: Any) -> None:
        pass

    @abstractmethod
    def get(self) -> dict:
        pass

    @abstractmethod
    def update(self, data: Any) -> None:
        pass

    @abstractmethod
    def delete(self, id: str) -> None:
        pass

    @abstractmethod
    def exists(self, email: str) -> bool:
        pass
