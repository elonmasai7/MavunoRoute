import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.base import TimestampMixin, UUIDPrimaryKeyMixin


class RouteStop(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "route_stops"

    route_plan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("route_plans.id"), nullable=False, index=True)
    stop_type: Mapped[str] = mapped_column(String(32), nullable=False)
    farmer_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("farmer_profiles.id"), nullable=True)
    buyer_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("buyer_profiles.id"), nullable=True)
    cold_hub_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("cold_hubs.id"), nullable=True)
    harvest_batch_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("harvest_batches.id"), nullable=True
    )
    sequence_number: Mapped[int] = mapped_column(Integer, nullable=False)
    latitude: Mapped[float] = mapped_column(nullable=False)
    longitude: Mapped[float] = mapped_column(nullable=False)
    planned_arrival_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    actual_arrival_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="PLANNED", index=True)
