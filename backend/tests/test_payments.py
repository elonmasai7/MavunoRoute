from uuid import uuid4

from app.services.mpesa_service import MpesaService
from app.services.payment_service import PaymentService


def test_payment_initiation(client, monkeypatch):
    class PaymentObj:
        id = uuid4()
        payer_user_id = str(uuid4())
        payee_user_id = str(uuid4())
        related_transport_job_id = None
        related_harvest_batch_id = None
        amount = 2000
        currency = "KES"
        provider = "MPESA"
        provider_reference = None
        status = "PENDING"
        created_at = "2026-05-21T00:00:00Z"
        updated_at = "2026-05-21T00:00:00Z"

    monkeypatch.setattr(PaymentService, "initiate", lambda self, payload: PaymentObj())
    response = client.post(
        "/api/v1/payments/initiate",
        json={"payer_user_id": str(uuid4()), "payee_user_id": str(uuid4()), "amount": 2000},
    )
    assert response.status_code == 200


def test_mpesa_callback(client, monkeypatch):
    monkeypatch.setattr(MpesaService, "callback", lambda self, payload, signature=None: {"accepted": True})
    response = client.post("/api/v1/mpesa/callback", json={"Body": {"stkCallback": {"CheckoutRequestID": "abc"}}})
    assert response.status_code == 200
    assert response.json()["data"]["accepted"] is True
