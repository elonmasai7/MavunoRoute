import uuid

from sqlalchemy import Enum, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.base import TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import PaymentStatus


class Payment(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "payments"

    payer_user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    payee_user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    related_transport_job_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("transport_jobs.id"), nullable=True, index=True
    )
    related_harvest_batch_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("harvest_batches.id"), nullable=True, index=True
    )
    amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(8), nullable=False, default="KES")
    provider: Mapped[str] = mapped_column(String(64), nullable=False, default="MPESA")
    provider_reference: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    status: Mapped[PaymentStatus] = mapped_column(Enum(PaymentStatus), nullable=False, default=PaymentStatus.PENDING, index=True)


class MpesaTransaction(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "mpesa_transactions"

    payment_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("payments.id"), nullable=False, index=True)
    checkout_request_id: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    merchant_request_id: Mapped[str] = mapped_column(String(255), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(32), nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    result_code: Mapped[str | None] = mapped_column(String(32), nullable=True)
    result_description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    provider_payload_json: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
