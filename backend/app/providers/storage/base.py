from abc import ABC, abstractmethod
from pathlib import Path


class StorageProviderInterface(ABC):
    @abstractmethod
    async def save(self, content: bytes, destination: str) -> str:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, destination: str) -> None:
        raise NotImplementedError
