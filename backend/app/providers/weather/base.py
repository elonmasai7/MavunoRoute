from abc import ABC, abstractmethod


class WeatherProviderInterface(ABC):
    @abstractmethod
    async def current_temperature(self, latitude: float, longitude: float) -> float | None:
        raise NotImplementedError
