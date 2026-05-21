from uuid import uuid4

from app.models.enums import VerificationStatus
from app.services.farmer_service import FarmerService


def test_create_farmer(client, monkeypatch):
    fake_id = uuid4()

    class FarmerObj:
        id = fake_id
        user_id = str(uuid4())
        county = "Nakuru"
        sub_county = "Naivasha"
        ward = "Biashara"
        village = "Karai"
        latitude = -0.7
        longitude = 36.4
        cooperative_id = None
        farm_size_acres = 2.5
        primary_crops = ["Tomato"]
        verification_status = VerificationStatus.PENDING
        created_at = "2026-05-21T00:00:00Z"
        updated_at = "2026-05-21T00:00:00Z"

    monkeypatch.setattr(FarmerService, "create", lambda self, payload: FarmerObj())

    response = client.post(
        "/api/v1/farmers",
        json={
            "user_id": str(uuid4()),
            "county": "Nakuru",
            "sub_county": "Naivasha",
            "ward": "Biashara",
            "village": "Karai",
            "latitude": -0.7,
            "longitude": 36.4,
            "farm_size_acres": 2.5,
            "primary_crops": ["Tomato"],
        },
    )
    assert response.status_code == 200
