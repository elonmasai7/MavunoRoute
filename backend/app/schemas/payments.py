from uuid import UUID

from pydantic import BaseModel, Field

from app.models.enums import PaymentStatus
from app.schemas.common import BaseReadSchema


class PaymentInitiate(BaseModel):
    payer_user_id: str
    payee_user_id: str
    related_transport_job_id: str | None = None
    related_harvest_batch_id: str | None = None
    amount: float = Field(gt=0)
    currency: str = "KES"
    provider: str = "MPESA"


class PaymentRead(BaseReadSchema):
    payer_user_id: UUID
    payee_user_id: UUID
    related_transport_job_id: UUID | None
    related_harvest_batch_id: UUID | None
    amount: float
    currency: str
    provider: str
    provider_reference: str | None
    status: PaymentStatus
