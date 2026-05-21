from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.base import TimestampMixin, UUIDPrimaryKeyMixin


class Crop(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "crops"

    name: Mapped[str] = mapped_column(String(128), nullable=False, unique=True, index=True)
    category: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    perishability_level: Mapped[int] = mapped_column(Integer, nullable=False)
    ideal_temperature_min: Mapped[float] = mapped_column(nullable=False)
    ideal_temperature_max: Mapped[float] = mapped_column(nullable=False)
    shelf_life_hours: Mapped[int] = mapped_column(Integer, nullable=False)
    handling_notes: Mapped[str] = mapped_column(String(500), nullable=False, default="")
