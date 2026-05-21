import base64
from datetime import UTC, datetime

import httpx

from app.config import get_settings
from app.providers.payments.base import PaymentProviderInterface

settings = get_settings()


class MpesaProvider(PaymentProviderInterface):
    def __init__(self):
        self.base_url = (
            "https://api.safaricom.co.ke"
            if settings.mpesa_environment == "production"
            else "https://sandbox.safaricom.co.ke"
        )

    async def _access_token(self) -> str:
        if not settings.mpesa_consumer_key or not settings.mpesa_consumer_secret:
            raise ValueError("M-Pesa provider not configured")

        creds = f"{settings.mpesa_consumer_key}:{settings.mpesa_consumer_secret}".encode()
        auth_header = base64.b64encode(creds).decode()
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.get(
                f"{self.base_url}/oauth/v1/generate?grant_type=client_credentials",
                headers={"Authorization": f"Basic {auth_header}"},
            )
            response.raise_for_status()
            return response.json().get("access_token")

    async def initiate_stk_push(self, phone_number: str, amount: float, reference: str) -> dict:
        if not all([settings.mpesa_shortcode, settings.mpesa_passkey, settings.mpesa_callback_url]):
            raise ValueError("M-Pesa provider not configured")

        access_token = await self._access_token()
        timestamp = datetime.now(UTC).strftime("%Y%m%d%H%M%S")
        password = base64.b64encode(f"{settings.mpesa_shortcode}{settings.mpesa_passkey}{timestamp}".encode()).decode()

        payload = {
            "BusinessShortCode": settings.mpesa_shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": int(amount),
            "PartyA": phone_number,
            "PartyB": settings.mpesa_shortcode,
            "PhoneNumber": phone_number,
            "CallBackURL": settings.mpesa_callback_url,
            "AccountReference": reference,
            "TransactionDesc": "MavunoRoute payment",
        }

        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.post(
                f"{self.base_url}/mpesa/stkpush/v1/processrequest",
                headers={"Authorization": f"Bearer {access_token}"},
                json=payload,
            )
            response.raise_for_status()
            return response.json()

    async def query_transaction(self, checkout_request_id: str) -> dict:
        return {"checkout_request_id": checkout_request_id}
