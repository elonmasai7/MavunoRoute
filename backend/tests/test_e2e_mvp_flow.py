from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.providers.routing.osrm_provider import OSRMRoutingProvider
from app.services.mpesa_service import MpesaService

FARMER_EMAIL = f"farmer_{uuid4().hex[:8]}@test.com"
BUYER_EMAIL = f"buyer_{uuid4().hex[:8]}@test.com"
ADMIN_EMAIL = f"admin_{uuid4().hex[:8]}@test.com"
TRANSPORTER_EMAIL = f"transporter_{uuid4().hex[:8]}@test.com"

PASSWORD = "StrongPass123!"


def register(client, name, email, phone, password, role):
    return client.post(
        "/api/v1/auth/register",
        json={"full_name": name, "email": email, "phone_number": phone, "password": password, "role": role},
    )


def login(client, email, password):
    return client.post("/api/v1/auth/login", json={"email": email, "password": password})


def auth_h(token):
    return {"Authorization": f"Bearer {token}"}


def assert_ok(resp, msg):
    assert resp.status_code == 200, f"{msg}: {resp.text}"


@pytest.mark.asyncio
async def test_full_mvp_flow(real_db_client: TestClient):
    monkeypatch = pytest.MonkeyPatch()

    # Mock OSRM routing provider
    async def fake_optimize_stops(self, points):
        return list(range(len(points)))

    async def fake_distance_matrix(self, points):
        n = len(points)
        return [[0.0 if i == j else 1000.0 for j in range(n)] for i in range(n)]

    async def fake_duration(self, points):
        return 60

    async def fake_polyline(self, points):
        return "mock_polyline"

    monkeypatch.setattr(OSRMRoutingProvider, "optimize_stops", fake_optimize_stops)
    monkeypatch.setattr(OSRMRoutingProvider, "get_distance_matrix", fake_distance_matrix)
    monkeypatch.setattr(OSRMRoutingProvider, "estimate_duration", fake_duration)
    monkeypatch.setattr(OSRMRoutingProvider, "get_route_polyline", fake_polyline)

    async def fake_stk_push(self, payment, phone_number):
        return {"CheckoutRequestID": "mock_ws_CO_" + uuid4().hex[:12], "MerchantRequestID": uuid4().hex[:16]}

    monkeypatch.setattr(MpesaService, "stk_push", fake_stk_push)

    # ===================================================================
    # 1. Register OPS_ADMIN (orchestrator — has all permissions)
    # ===================================================================
    resp = register(real_db_client, "Admin Ops", ADMIN_EMAIL, "+254700300003", PASSWORD, "OPS_ADMIN")
    assert_ok(resp, "Admin register")
    resp = login(real_db_client, ADMIN_EMAIL, PASSWORD)
    assert_ok(resp, "Admin login")
    admin_token = resp.json()["data"]["access_token"]

    # ===================================================================
    # 2. Register FARMER user & create profile (via admin)
    # ===================================================================
    resp = register(real_db_client, "Farmer Jane", FARMER_EMAIL, "+254700100001", PASSWORD, "FARMER")
    assert_ok(resp, "Farmer register")
    farmer_user_id = resp.json()["data"]["user_id"]

    resp = real_db_client.post(
        "/api/v1/farmers",
        json={
            "user_id": farmer_user_id,
            "county": "Kiambu", "sub_county": "Gatundu South",
            "ward": "Ndarugu", "village": "Kwa Maiko",
            "latitude": -1.0542, "longitude": 36.8453,
            "farm_size_acres": 3.5, "primary_crops": ["Tomatoes", "Kale"],
        },
        headers=auth_h(admin_token),
    )
    assert_ok(resp, "Farmer profile creation")
    farmer_profile_id = resp.json()["data"]["id"]

    resp = login(real_db_client, FARMER_EMAIL, PASSWORD)
    assert_ok(resp, "Farmer login")
    farmer_token = resp.json()["data"]["access_token"]

    # ===================================================================
    # 3. Create crop (any authenticated user can)
    # ===================================================================
    resp = real_db_client.post(
        "/api/v1/crops",
        json={
            "name": "Tomato", "category": "Vegetables",
            "perishability_level": 8, "ideal_temperature_min": 4,
            "ideal_temperature_max": 8, "shelf_life_hours": 36,
            "handling_notes": "Handle with care, stack max 3 crates",
        },
        headers=auth_h(admin_token),
    )
    assert_ok(resp, "Crop creation")
    crop_id = resp.json()["data"]["id"]

    # ===================================================================
    # 4. Create harvest batch (farmer has harvests:write)
    # ===================================================================
    resp = real_db_client.post(
        "/api/v1/harvest-batches",
        json={
            "farmer_id": farmer_profile_id,
            "crop_id": crop_id,
            "quantity_kg": 500.0,
            "expected_harvest_datetime": "2026-05-22T06:00:00Z",
            "grade": "A", "packaging_type": "CRATE",
            "asking_price_per_kg": 65.0,
            "latitude": -1.0542, "longitude": 36.8453,
        },
        headers=auth_h(farmer_token),
    )
    assert_ok(resp, "Harvest batch creation")
    harvest_batch_id = resp.json()["data"]["id"]

    # ===================================================================
    # 5. Register BUYER user, create profile & demand (buyer has permissions)
    # ===================================================================
    resp = register(real_db_client, "Buyer Co", BUYER_EMAIL, "+254700200002", PASSWORD, "BUYER")
    assert_ok(resp, "Buyer register")
    buyer_user_id = resp.json()["data"]["user_id"]

    resp = login(real_db_client, BUYER_EMAIL, PASSWORD)
    assert_ok(resp, "Buyer login")
    buyer_token = resp.json()["data"]["access_token"]

    resp = real_db_client.post(
        "/api/v1/buyers",
        json={
            "user_id": buyer_user_id,
            "business_name": "Fresh Produce Ltd", "business_type": "RETAILER",
            "kra_pin": "P051234567Z", "county": "Nairobi",
            "delivery_address": "123 Kimathi Street, Nairobi",
            "latitude": -1.2921, "longitude": 36.8219,
        },
        headers=auth_h(buyer_token),
    )
    assert_ok(resp, "Buyer profile creation")
    buyer_profile_id = resp.json()["data"]["id"]

    resp = real_db_client.post(
        "/api/v1/buyer-demands",
        json={
            "buyer_id": buyer_profile_id, "crop_id": crop_id,
            "quantity_kg": 300.0, "desired_grade": "A",
            "max_price_per_kg": 70.0,
            "required_delivery_datetime": "2026-05-23T10:00:00Z",
            "delivery_latitude": -1.2921, "delivery_longitude": 36.8219,
        },
        headers=auth_h(buyer_token),
    )
    assert_ok(resp, "Buyer demand creation")
    buyer_demand_id = resp.json()["data"]["id"]

    # ===================================================================
    # 6. Run matching (admin)
    # ===================================================================
    resp = real_db_client.post(
        "/api/v1/matching/harvest-to-demand",
        json={"buyer_demand_id": buyer_demand_id},
        headers=auth_h(admin_token),
    )
    assert_ok(resp, "Matching")
    matches = resp.json()["data"]["matches"]
    assert len(matches) >= 1, "Expected at least one match"

    # ===================================================================
    # 7. Register TRANSPORTER user & create profile, vehicle (via admin)
    # ===================================================================
    resp = register(real_db_client, "Transporter Joe", TRANSPORTER_EMAIL, "+254700400004", PASSWORD, "TRANSPORTER")
    assert_ok(resp, "Transporter register")
    transporter_user_id = resp.json()["data"]["user_id"]

    resp = real_db_client.post(
        "/api/v1/transporters",
        json={
            "user_id": transporter_user_id,
            "business_name": "Quick Haul Logistics",
            "license_number": "TLS-2026-0042",
            "phone_number": "+254700400004",
            "county": "Kiambu",
        },
        headers=auth_h(admin_token),
    )
    assert_ok(resp, "Transporter creation")
    transporter_id = resp.json()["data"]["id"]

    resp = real_db_client.post(
        "/api/v1/vehicles",
        json={
            "transporter_id": transporter_id,
            "plate_number": "KCA 123T",
            "vehicle_type": "LIGHT_TRUCK",
            "capacity_kg": 2000.0,
            "has_refrigeration": True,
            "temperature_min": 2.0, "temperature_max": 10.0,
            "insurance_status": "ACTIVE", "inspection_status": "PASSED",
        },
        headers=auth_h(admin_token),
    )
    assert_ok(resp, "Vehicle creation")
    vehicle_id = resp.json()["data"]["id"]

    resp = login(real_db_client, TRANSPORTER_EMAIL, PASSWORD)
    assert_ok(resp, "Transporter login")
    transporter_token = resp.json()["data"]["access_token"]

    # ===================================================================
    # 8. Plan route (admin — triggers transport jobs automatically)
    # ===================================================================
    resp = real_db_client.post(
        "/api/v1/routes/plan",
        json={
            "harvest_batch_ids": [harvest_batch_id],
            "destination_buyer_id": buyer_profile_id,
            "vehicle_id": vehicle_id,
        },
        headers=auth_h(admin_token),
    )
    assert_ok(resp, "Route planning")
    route_result = resp.json()["data"]
    route_id = route_result["route_id"]
    assert route_result["jobs_created"] == 1

    # ===================================================================
    # 9. Record proof of delivery (transporter has proofs:write)
    # ===================================================================
    resp = real_db_client.get(
        "/api/v1/transport-jobs",
        params={"route_plan_id": route_id},
        headers=auth_h(admin_token),
    )
    assert_ok(resp, "List transport jobs")
    jobs_data = resp.json()["data"]
    assert len(jobs_data) >= 1, "Expected at least one transport job"
    transport_job_id = jobs_data[0]["id"]

    resp = real_db_client.post(
        "/api/v1/proof-events",
        json={
            "transport_job_id": transport_job_id,
            "event_type": "DELIVERY",
            "qr_code": uuid4().hex[:16].upper(),
            "photo_url": None, "signature_url": None,
            "latitude": -1.2921, "longitude": 36.8219,
            "notes": "Delivered to Fresh Produce Ltd loading bay",
        },
        headers=auth_h(transporter_token),
    )
    assert_ok(resp, "Proof event")
    assert resp.json()["data"]["qr_code"] is not None

    # ===================================================================
    # 10. Initiate payment (buyer has payments:write)
    # ===================================================================
    resp = real_db_client.post(
        "/api/v1/payments/initiate",
        json={
            "payer_user_id": buyer_user_id,
            "payee_user_id": farmer_user_id,
            "amount": 19500.0, "currency": "KES", "provider": "MPESA",
        },
        headers=auth_h(buyer_token),
    )
    assert_ok(resp, "Payment initiation")
    payment_id = resp.json()["data"]["id"]

    # ===================================================================
    # 11. Dashboard reports (admin)
    # ===================================================================
    resp = real_db_client.get(
        "/api/v1/reports/dashboard",
        headers=auth_h(admin_token),
    )
    assert_ok(resp, "Dashboard reports")
    metrics = resp.json()["data"]
    assert metrics["total_farmers"] >= 1
    assert metrics["total_buyers"] >= 1
    assert metrics["active_harvest_batches"] >= 1

    # ===================================================================
    # 12. Verify end-to-end consistency
    # ===================================================================
    resp = real_db_client.get(f"/api/v1/harvest-batches/{harvest_batch_id}", headers=auth_h(admin_token))
    assert_ok(resp, "Fetch harvest batch")
    assert resp.json()["data"]["status"] == "DRAFT"

    resp = real_db_client.get(f"/api/v1/payments/{payment_id}", headers=auth_h(admin_token))
    assert_ok(resp, "Fetch payment")
    assert resp.json()["data"]["amount"] == 19500.0

    monkeypatch.undo()
