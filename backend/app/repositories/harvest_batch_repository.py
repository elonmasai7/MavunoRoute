from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.enums import HarvestBatchStatus
from app.models.harvest_batch import HarvestBatch


class HarvestBatchRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, model: HarvestBatch) -> HarvestBatch:
        self.db.add(model)
        self.db.flush()
        self.db.refresh(model)
        return model

    def get(self, batch_id: UUID) -> HarvestBatch | None:
        return self.db.get(HarvestBatch, batch_id)

    def list(self, page: int, per_page: int) -> tuple[list[HarvestBatch], int]:
        stmt = select(HarvestBatch).offset((page - 1) * per_page).limit(per_page)
        rows = self.db.scalars(stmt).all()
        total = self.db.query(HarvestBatch).count()
        return rows, total

    def list_open_for_matching(self, crop_id: UUID) -> list[HarvestBatch]:
        return self.db.scalars(
            select(HarvestBatch).where(
                HarvestBatch.crop_id == crop_id,
                HarvestBatch.status.in_(
                    [HarvestBatchStatus.READY, HarvestBatchStatus.DRAFT, HarvestBatchStatus.MATCHED]
                ),
            )
        ).all()
