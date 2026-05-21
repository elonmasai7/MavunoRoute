from abc import ABC, abstractmethod


class PaymentProviderInterface(ABC):
    @abstractmethod
    async def initiate_stk_push(self, phone_number: str, amount: float, reference: str) -> dict:
        raise NotImplementedError

    @abstractmethod
    async def query_transaction(self, checkout_request_id: str) -> dict:
        raise NotImplementedError
