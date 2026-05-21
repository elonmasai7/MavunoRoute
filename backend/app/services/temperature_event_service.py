from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.temperature_event import TemperatureEvent
from app.schemas.temperature_events import TemperatureEventCreate


class TemperatureEventService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, payload: TemperatureEventCreate):
        data = payload.model_dump()
        if data.get("recorded_at") is None:
            data.pop("recorded_at")
        event = TemperatureEvent(**data)
        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)
        return event

    def list(self, page: int, per_page: int):
        rows = self.db.scalars(select(TemperatureEvent).offset((page - 1) * per_page).limit(per_page)).all()
        total = self.db.query(TemperatureEvent).count()
        return rows, total

    def get(self, event_id: UUID):
        event = self.db.get(TemperatureEvent, event_id)
        if not event:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Temperature event not found")
        return event
