from uuid import uuid4

from app.services.harvest_batch_service import HarvestBatchService


def test_create_harvest_batch(client, monkeypatch):
    class BatchObj:
        id = uuid4()
        farmer_id = str(uuid4())
        crop_id = str(uuid4())
        quantity_kg = 120.5
        expected_harvest_datetime = "2026-05-21T10:00:00Z"
        actual_harvest_datetime = None
        grade = "A"
        packaging_type = "Crate"
        asking_price_per_kg = 42.0
        latitude = -1.2
        longitude = 36.8
        status = "DRAFT"
        spoilage_risk_score = 0
        created_at = "2026-05-21T00:00:00Z"
        updated_at = "2026-05-21T00:00:00Z"

    monkeypatch.setattr(HarvestBatchService, "create", lambda self, payload: BatchObj())
    response = client.post(
        "/api/v1/harvest-batches",
        json={
            "farmer_id": str(uuid4()),
            "crop_id": str(uuid4()),
            "quantity_kg": 120.5,
            "expected_harvest_datetime": "2026-05-21T10:00:00Z",
            "grade": "A",
            "packaging_type": "Crate",
            "asking_price_per_kg": 42,
            "latitude": -1.2,
            "longitude": 36.8,
        },
    )
    assert response.status_code == 200


def test_calculate_spoilage_risk(client, monkeypatch):
    async def fake_calculate(self, batch_id, route_duration_minutes=None):
        return {
            "harvest_batch_id": str(batch_id),
            "risk_score": 70,
            "risk_level": "HIGH",
            "recommended_action": "Dispatch within 3 hours",
            "estimated_value_at_risk": 12000,
            "explanation": ["High perishability"],
        }

    monkeypatch.setattr(HarvestBatchService, "calculate_spoilage_risk", fake_calculate)
    response = client.post(f"/api/v1/harvest-batches/{uuid4()}/calculate-spoilage-risk")
    assert response.status_code == 200
    assert response.json()["data"]["risk_level"] == "HIGH"
