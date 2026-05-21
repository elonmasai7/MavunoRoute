import uuid

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.base import TimestampMixin, UUIDPrimaryKeyMixin


class ColdHub(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "cold_hubs"

    operator_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    county: Mapped[str] = mapped_column(String(128), nullable=False)
    latitude: Mapped[float] = mapped_column(nullable=False)
    longitude: Mapped[float] = mapped_column(nullable=False)
    total_capacity_kg: Mapped[float] = mapped_column(nullable=False)
    available_capacity_kg: Mapped[float] = mapped_column(nullable=False)
    temperature_min: Mapped[float] = mapped_column(nullable=False)
    temperature_max: Mapped[float] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
