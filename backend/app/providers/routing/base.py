from abc import ABC, abstractmethod


class RoutingProviderInterface(ABC):
    @abstractmethod
    async def get_distance_matrix(self, points: list[tuple[float, float]]) -> list[list[float]]:
        raise NotImplementedError

    @abstractmethod
    async def optimize_stops(self, points: list[tuple[float, float]]) -> list[int]:
        raise NotImplementedError

    @abstractmethod
    async def get_route_polyline(self, points: list[tuple[float, float]]) -> str:
        raise NotImplementedError

    @abstractmethod
    async def estimate_duration(self, points: list[tuple[float, float]]) -> int:
        raise NotImplementedError
