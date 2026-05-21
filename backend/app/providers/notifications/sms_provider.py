from abc import ABC, abstractmethod


class SMSProviderInterface(ABC):
    @abstractmethod
    async def send(self, phone_number: str, message: str) -> dict:
        raise NotImplementedError
