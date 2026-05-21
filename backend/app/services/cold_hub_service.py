from math import sqrt
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.cold_hub import ColdHub
from app.schemas.cold_hubs import ColdHubCreate, ColdHubUpdate


class ColdHubService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, payload: ColdHubCreate):
        hub = ColdHub(**payload.model_dump())
        self.db.add(hub)
        self.db.commit()
        self.db.refresh(hub)
        return hub

    def list(self, page: int, per_page: int):
        rows = self.db.scalars(select(ColdHub).offset((page - 1) * per_page).limit(per_page)).all()
        total = self.db.query(ColdHub).count()
        return rows, total

    def get(self, hub_id: UUID):
        hub = self.db.get(ColdHub, hub_id)
        if not hub:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cold hub not found")
        return hub

    def update(self, hub_id: UUID, payload: ColdHubUpdate):
        hub = self.get(hub_id)
        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(hub, key, value)
        self.db.commit()
        self.db.refresh(hub)
        return hub

    def update_capacity(self, hub_id: UUID, available_capacity_kg: float):
        hub = self.get(hub_id)
        if available_capacity_kg > hub.total_capacity_kg:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Available capacity exceeds total capacity")
        hub.available_capacity_kg = available_capacity_kg
        self.db.commit()
        self.db.refresh(hub)
        return hub

    def nearby(self, latitude: float, longitude: float, radius_km: float):
        hubs = self.db.scalars(select(ColdHub).where(ColdHub.is_active.is_(True))).all()
        result = []
        for hub in hubs:
            distance = sqrt((hub.latitude - latitude) ** 2 + (hub.longitude - longitude) ** 2) * 111
            if distance <= radius_km:
                result.append((hub, distance))
        result.sort(key=lambda item: item[1])
        return result

    def check_in(self, hub_id: UUID, quantity_kg: float):
        hub = self.get(hub_id)
        if hub.available_capacity_kg < quantity_kg:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient cold hub capacity")
        hub.available_capacity_kg -= quantity_kg
        self.db.commit()
        self.db.refresh(hub)
        return hub

    def check_out(self, hub_id: UUID, quantity_kg: float):
        hub = self.get(hub_id)
        hub.available_capacity_kg = min(hub.total_capacity_kg, hub.available_capacity_kg + quantity_kg)
        self.db.commit()
        self.db.refresh(hub)
        return hub
