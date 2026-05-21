import uuid
from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.base import TimestampMixin, UUIDPrimaryKeyMixin


class TemperatureEvent(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "temperature_events"

    harvest_batch_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("harvest_batches.id"), nullable=False, index=True
    )
    transport_job_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("transport_jobs.id"), nullable=True)
    cold_hub_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("cold_hubs.id"), nullable=True)
    temperature_celsius: Mapped[float] = mapped_column(nullable=False)
    humidity: Mapped[float | None] = mapped_column(nullable=True)
    source: Mapped[str] = mapped_column(String(64), nullable=False)
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC))
