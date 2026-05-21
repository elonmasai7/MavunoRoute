from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.farmer import FarmerProfile
from app.repositories.farmer_repository import FarmerRepository
from app.schemas.farmers import FarmerCreate, FarmerUpdate


class FarmerService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = FarmerRepository(db)

    def create(self, payload: FarmerCreate) -> FarmerProfile:
        farmer = FarmerProfile(**payload.model_dump())
        self.repo.create(farmer)
        self.db.commit()
        return farmer

    def list(self, page: int, per_page: int):
        return self.repo.list(page, per_page)

    def get(self, farmer_id: UUID):
        farmer = self.repo.get(farmer_id)
        if not farmer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Farmer not found")
        return farmer

    def update(self, farmer_id: UUID, payload: FarmerUpdate):
        farmer = self.get(farmer_id)
        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(farmer, key, value)
        self.db.commit()
        self.db.refresh(farmer)
        return farmer
