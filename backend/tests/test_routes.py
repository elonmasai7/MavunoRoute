from uuid import uuid4

from app.services.route_optimization_service import RouteOptimizationService


def test_route_planning(client, monkeypatch):
    async def fake_plan(self, payload):
        return {
            "route_id": str(uuid4()),
            "route_code": "MR-202605210001",
            "total_distance_km": 32.5,
            "estimated_duration_minutes": 82,
            "route_polyline": "abc123",
            "jobs_created": 1,
        }

    monkeypatch.setattr(RouteOptimizationService, "plan_route", fake_plan)
    response = client.post(
        "/api/v1/routes/plan",
        json={
            "harvest_batch_ids": [str(uuid4())],
            "destination_buyer_id": str(uuid4()),
            "vehicle_id": str(uuid4()),
        },
    )
    assert response.status_code == 200
    assert response.json()["data"]["jobs_created"] == 1
