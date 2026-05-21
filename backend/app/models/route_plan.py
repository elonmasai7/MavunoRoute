import uuid

from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.base import TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import RouteStatus


class RoutePlan(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "route_plans"

    route_code: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, index=True)
    origin_county: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    destination_county: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    vehicle_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("vehicles.id"), nullable=True)
    transporter_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("transporter_profiles.id"), nullable=True
    )
    assigned_driver_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    total_distance_km: Mapped[float] = mapped_column(nullable=False, default=0)
    estimated_duration_minutes: Mapped[int] = mapped_column(nullable=False, default=0)
    route_polyline: Mapped[str | None] = mapped_column(String, nullable=True)
    route_provider: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[RouteStatus] = mapped_column(Enum(RouteStatus), nullable=False, default=RouteStatus.PLANNED, index=True)
