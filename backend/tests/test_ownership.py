from types import SimpleNamespace
from uuid import uuid4

from app.dependencies import get_current_user
from app.services.buyer_service import BuyerService
from app.services.farmer_service import FarmerService


def test_farmer_cannot_view_other_farmer_profile(client, monkeypatch):
    app = client.app
    farmer_user_id = uuid4()
    other_user_id = uuid4()
    app.dependency_overrides[get_current_user] = lambda: SimpleNamespace(id=farmer_user_id, role="FARMER", is_active=True)

    class FarmerObj:
        id = uuid4()
        user_id = other_user_id
        county = "Nakuru"
        sub_county = "Naivasha"
        ward = "Biashara"
        village = "Karai"
        latitude = -0.7
        longitude = 36.4
        cooperative_id = None
        farm_size_acres = 2.5
        primary_crops = ["Tomato"]
        verification_status = "PENDING"
        created_at = "2026-05-21T00:00:00Z"
        updated_at = "2026-05-21T00:00:00Z"

    monkeypatch.setattr(FarmerService, "get", lambda self, farmer_id: FarmerObj())

    response = client.get(f"/api/v1/farmers/{uuid4()}")
    assert response.status_code == 403


def test_buyer_cannot_update_other_buyer_profile(client, monkeypatch):
    app = client.app
    buyer_user_id = uuid4()
    other_user_id = uuid4()
    app.dependency_overrides[get_current_user] = lambda: SimpleNamespace(id=buyer_user_id, role="BUYER", is_active=True)

    class BuyerObj:
        id = uuid4()
        user_id = other_user_id
        business_name = "Market One"
        business_type = "Retail"
        kra_pin = None
        county = "Nairobi"
        delivery_address = "Muthurwa"
        latitude = -1.28
        longitude = 36.82
        verification_status = "PENDING"
        created_at = "2026-05-21T00:00:00Z"
        updated_at = "2026-05-21T00:00:00Z"

    monkeypatch.setattr(BuyerService, "get", lambda self, buyer_id: BuyerObj())

    response = client.patch(f"/api/v1/buyers/{uuid4()}", json={"business_name": "New Name"})
    assert response.status_code == 403
