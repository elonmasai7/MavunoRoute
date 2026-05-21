import httpx

from app.providers.routing.base import RoutingProviderInterface


class OSRMRoutingProvider(RoutingProviderInterface):
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    async def get_distance_matrix(self, points: list[tuple[float, float]]) -> list[list[float]]:
        coords = ";".join(f"{lon},{lat}" for lat, lon in points)
        url = f"{self.base_url}/table/v1/driving/{coords}"
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.get(url, params={"annotations": "distance"})
            resp.raise_for_status()
            return resp.json().get("distances", [])

    async def optimize_stops(self, points: list[tuple[float, float]]) -> list[int]:
        coords = ";".join(f"{lon},{lat}" for lat, lon in points)
        url = f"{self.base_url}/trip/v1/driving/{coords}"
        async with httpx.AsyncClient(timeout=20) as client:
            resp = await client.get(url, params={"source": "first", "destination": "last", "roundtrip": "false"})
            resp.raise_for_status()
            waypoints = resp.json().get("waypoints", [])
            return [item["waypoint_index"] for item in sorted(waypoints, key=lambda wp: wp["waypoint_index"])]

    async def get_route_polyline(self, points: list[tuple[float, float]]) -> str:
        coords = ";".join(f"{lon},{lat}" for lat, lon in points)
        url = f"{self.base_url}/route/v1/driving/{coords}"
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.get(url, params={"overview": "full", "geometries": "polyline"})
            resp.raise_for_status()
            routes = resp.json().get("routes", [])
            if not routes:
                return ""
            return routes[0].get("geometry", "")

    async def estimate_duration(self, points: list[tuple[float, float]]) -> int:
        coords = ";".join(f"{lon},{lat}" for lat, lon in points)
        url = f"{self.base_url}/route/v1/driving/{coords}"
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.get(url, params={"overview": "false"})
            resp.raise_for_status()
            routes = resp.json().get("routes", [])
            if not routes:
                return 0
            return int(routes[0].get("duration", 0) / 60)
