from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.crop import Crop
from app.models.harvest_batch import HarvestBatch
from app.repositories.harvest_batch_repository import HarvestBatchRepository
from app.schemas.harvest_batches import HarvestBatchCreate, HarvestBatchUpdate
from app.services.spoilage_risk_service import SpoilageRiskService
from app.services.weather_service import WeatherService


class HarvestBatchService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = HarvestBatchRepository(db)
        self.spoilage_service = SpoilageRiskService(db)
        self.weather_service = WeatherService()

    def create(self, payload: HarvestBatchCreate):
        batch = HarvestBatch(**payload.model_dump())
        self.repo.create(batch)
        self.db.commit()
        self.db.refresh(batch)
        return batch

    def list(self, page: int, per_page: int):
        return self.repo.list(page, per_page)

    def get(self, batch_id: UUID):
        batch = self.repo.get(batch_id)
        if not batch:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Harvest batch not found")
        return batch

    def update(self, batch_id: UUID, payload: HarvestBatchUpdate):
        batch = self.get(batch_id)
        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(batch, key, value)
        self.db.commit()
        self.db.refresh(batch)
        return batch

    async def calculate_spoilage_risk(self, batch_id: UUID, route_duration_minutes: int | None = None):
        batch = self.get(batch_id)
        crop = self.db.get(Crop, batch.crop_id)
        if not crop:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Crop not found for batch")

        weather_temp = await self.weather_service.get_current_temperature(batch.latitude, batch.longitude)
        score_payload = self.spoilage_service.calculate(batch, crop, weather_temp, route_duration_minutes)
        batch.spoilage_risk_score = score_payload["risk_score"]
        self.db.commit()
        return score_payload
