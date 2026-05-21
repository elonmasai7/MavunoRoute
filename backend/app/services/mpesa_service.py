import hashlib
import hmac
import json

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.config import get_settings
from app.models.integration_log import ApiIntegrationLog
from app.models.payment import MpesaTransaction, Payment
from app.models.enums import PaymentStatus
from app.providers.payments.mpesa_provider import MpesaProvider

settings = get_settings()


class MpesaService:
    def __init__(self, db: Session):
        self.db = db
        self.provider = MpesaProvider()

    async def stk_push(self, payment: Payment, phone_number: str) -> dict:
        try:
            response = await self.provider.initiate_stk_push(phone_number, float(payment.amount), str(payment.id))
        except ValueError as exc:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc)) from exc

        checkout_request_id = response.get("CheckoutRequestID")
        if not checkout_request_id:
            raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Invalid M-Pesa response")

        txn = MpesaTransaction(
            payment_id=payment.id,
            checkout_request_id=checkout_request_id,
            merchant_request_id=response.get("MerchantRequestID", ""),
            phone_number=phone_number,
            amount=payment.amount,
            provider_payload_json=response,
        )
        self.db.add(txn)
        payment.provider_reference = checkout_request_id
        payment.status = PaymentStatus.PROCESSING
        self.db.add(ApiIntegrationLog(provider="MPESA", request_type="STK_PUSH", status="SUCCESS", response_code=200))
        self.db.commit()

        return response

    def callback(self, payload: dict, signature: str | None = None) -> dict:
        if settings.mpesa_callback_secret:
            if not signature:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing callback signature")
            serialized = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
            digest = hmac.new(settings.mpesa_callback_secret.encode(), serialized, hashlib.sha256).hexdigest()
            if not hmac.compare_digest(digest, signature):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid callback signature")

        stk_callback = payload.get("Body", {}).get("stkCallback", {})
        checkout_request_id = stk_callback.get("CheckoutRequestID")
        if not checkout_request_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing CheckoutRequestID")

        txn = self.db.query(MpesaTransaction).filter(MpesaTransaction.checkout_request_id == checkout_request_id).first()
        if not txn:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")

        result_code = str(stk_callback.get("ResultCode", "1"))
        txn.result_code = result_code
        txn.result_description = stk_callback.get("ResultDesc", "")
        txn.provider_payload_json = payload

        payment = self.db.get(Payment, txn.payment_id)
        if payment:
            payment.status = PaymentStatus.PAID if result_code == "0" else PaymentStatus.FAILED

        self.db.add(ApiIntegrationLog(provider="MPESA", request_type="CALLBACK", status="SUCCESS", response_code=200))
        self.db.commit()
        return {"accepted": True}
