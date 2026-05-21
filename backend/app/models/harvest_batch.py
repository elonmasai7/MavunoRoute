import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.base import TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import HarvestBatchStatus


class HarvestBatch(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "harvest_batches"

    farmer_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("farmer_profiles.id"), nullable=False, index=True)
    crop_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("crops.id"), nullable=False, index=True)
    quantity_kg: Mapped[float] = mapped_column(nullable=False)
    expected_harvest_datetime: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    actual_harvest_datetime: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    grade: Mapped[str] = mapped_column(String(64), nullable=False)
    packaging_type: Mapped[str] = mapped_column(String(64), nullable=False)
    asking_price_per_kg: Mapped[float] = mapped_column(nullable=False)
    latitude: Mapped[float] = mapped_column(nullable=False)
    longitude: Mapped[float] = mapped_column(nullable=False)
    status: Mapped[HarvestBatchStatus] = mapped_column(
        Enum(HarvestBatchStatus), nullable=False, default=HarvestBatchStatus.DRAFT, index=True
    )
    spoilage_risk_score: Mapped[int] = mapped_column(nullable=False, default=0)
