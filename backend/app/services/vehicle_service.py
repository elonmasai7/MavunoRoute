from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.vehicle import Vehicle
from app.schemas.vehicles import VehicleCreate, VehicleUpdate


class VehicleService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, payload: VehicleCreate):
        vehicle = Vehicle(**payload.model_dump())
        self.db.add(vehicle)
        self.db.commit()
        self.db.refresh(vehicle)
        return vehicle

    def list(self, page: int, per_page: int):
        rows = self.db.scalars(select(Vehicle).offset((page - 1) * per_page).limit(per_page)).all()
        total = self.db.query(Vehicle).count()
        return rows, total

    def get(self, vehicle_id: UUID):
        vehicle = self.db.get(Vehicle, vehicle_id)
        if not vehicle:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found")
        return vehicle

    def update(self, vehicle_id: UUID, payload: VehicleUpdate):
        vehicle = self.get(vehicle_id)
        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(vehicle, key, value)
        self.db.commit()
        self.db.refresh(vehicle)
        return vehicle

    def set_availability(self, vehicle_id: UUID, is_available: bool):
        vehicle = self.get(vehicle_id)
        vehicle.is_available = is_available
        self.db.commit()
        self.db.refresh(vehicle)
        return vehicle

    def available(self, page: int, per_page: int):
        rows = self.db.scalars(
            select(Vehicle).where(Vehicle.is_available.is_(True)).offset((page - 1) * per_page).limit(per_page)
        ).all()
        total = self.db.query(Vehicle).filter(Vehicle.is_available.is_(True)).count()
        return rows, total
