from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.crop import Crop
from app.schemas.crops import CropCreate, CropUpdate


class CropService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, payload: CropCreate) -> Crop:
        crop = Crop(**payload.model_dump())
        self.db.add(crop)
        self.db.commit()
        self.db.refresh(crop)
        return crop

    def list(self, page: int, per_page: int):
        rows = self.db.scalars(select(Crop).offset((page - 1) * per_page).limit(per_page)).all()
        total = self.db.query(Crop).count()
        return rows, total

    def get(self, crop_id: UUID) -> Crop:
        crop = self.db.get(Crop, crop_id)
        if not crop:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Crop not found")
        return crop

    def update(self, crop_id: UUID, payload: CropUpdate):
        crop = self.get(crop_id)
        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(crop, key, value)
        self.db.commit()
        self.db.refresh(crop)
        return crop

    def delete(self, crop_id: UUID):
        crop = self.get(crop_id)
        self.db.delete(crop)
        self.db.commit()
