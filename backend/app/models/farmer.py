import uuid

from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.base import TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import VerificationStatus


class FarmerProfile(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "farmer_profiles"

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, unique=True, index=True)
    national_id_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)
    county: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    sub_county: Mapped[str] = mapped_column(String(128), nullable=False)
    ward: Mapped[str] = mapped_column(String(128), nullable=False)
    village: Mapped[str] = mapped_column(String(128), nullable=False)
    latitude: Mapped[float] = mapped_column(nullable=False)
    longitude: Mapped[float] = mapped_column(nullable=False)
    cooperative_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("cooperatives.id"), nullable=True)
    farm_size_acres: Mapped[float] = mapped_column(nullable=False)
    primary_crops: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False, default=list)
    verification_status: Mapped[VerificationStatus] = mapped_column(
        Enum(VerificationStatus), nullable=False, default=VerificationStatus.PENDING
    )
