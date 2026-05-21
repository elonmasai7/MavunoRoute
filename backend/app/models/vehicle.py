import uuid

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.base import TimestampMixin, UUIDPrimaryKeyMixin


class Vehicle(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "vehicles"

    transporter_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("transporter_profiles.id"), nullable=False, index=True
    )
    plate_number: Mapped[str] = mapped_column(String(32), nullable=False, unique=True, index=True)
    vehicle_type: Mapped[str] = mapped_column(String(64), nullable=False)
    capacity_kg: Mapped[float] = mapped_column(nullable=False)
    has_refrigeration: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    temperature_min: Mapped[float | None] = mapped_column(nullable=True)
    temperature_max: Mapped[float | None] = mapped_column(nullable=True)
    insurance_status: Mapped[str] = mapped_column(String(64), nullable=False)
    inspection_status: Mapped[str] = mapped_column(String(64), nullable=False)
    is_available: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, index=True)
