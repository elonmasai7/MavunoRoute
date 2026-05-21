from uuid import uuid4

from app.services.transport_job_service import TransportJobService


def test_transport_job_creation(client, monkeypatch):
    class JobObj:
        id = uuid4()
        route_plan_id = str(uuid4())
        harvest_batch_id = str(uuid4())
        buyer_demand_id = None
        transporter_id = str(uuid4())
        vehicle_id = str(uuid4())
        pickup_status = "PENDING"
        delivery_status = "PENDING"
        agreed_transport_fee = 2500
        created_at = "2026-05-21T00:00:00Z"
        updated_at = "2026-05-21T00:00:00Z"

    monkeypatch.setattr(TransportJobService, "create", lambda self, payload: JobObj())
    response = client.post(
        "/api/v1/transport-jobs",
        json={
            "route_plan_id": str(uuid4()),
            "harvest_batch_id": str(uuid4()),
            "transporter_id": str(uuid4()),
            "vehicle_id": str(uuid4()),
            "agreed_transport_fee": 2500,
        },
    )
    assert response.status_code == 200
