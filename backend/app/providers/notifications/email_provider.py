from abc import ABC, abstractmethod


class EmailProviderInterface(ABC):
    @abstractmethod
    async def send(self, recipient_email: str, subject: str, message: str) -> dict:
        raise NotImplementedError
