from math import sqrt

from sqlalchemy.orm import Session

from app.models.buyer_demand import BuyerDemand
from app.models.harvest_batch import HarvestBatch
from app.models.enums import HarvestBatchStatus
from app.repositories.buyer_repository import BuyerRepository
from app.repositories.harvest_batch_repository import HarvestBatchRepository


class MatchingService:
    def __init__(self, db: Session):
        self.db = db
        self.buyer_repo = BuyerRepository(db)
        self.harvest_repo = HarvestBatchRepository(db)

    @staticmethod
    def _distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        # Lightweight distance approximation for ranking.
        return sqrt((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2) * 111

    def match_harvest_to_demand(self, demand: BuyerDemand) -> dict:
        candidate_batches: list[HarvestBatch] = self.harvest_repo.list_open_for_matching(demand.crop_id)
        matches = []

        for batch in candidate_batches:
            if batch.status == HarvestBatchStatus.CANCELLED:
                continue
            if batch.grade.lower() != demand.desired_grade.lower():
                continue
            if batch.asking_price_per_kg > demand.max_price_per_kg:
                continue

            quantity_score = min((batch.quantity_kg / demand.quantity_kg) * 30, 30)
            price_gap = max(demand.max_price_per_kg - batch.asking_price_per_kg, 0)
            price_score = min(price_gap * 3, 20)
            distance = self._distance_km(
                batch.latitude,
                batch.longitude,
                demand.delivery_latitude,
                demand.delivery_longitude,
            )
            distance_score = max(25 - min(distance, 25), 0)
            urgency_score = max(20 - min(batch.spoilage_risk_score / 5, 20), 0)

            match_score = int(quantity_score + price_score + distance_score + urgency_score)

            matches.append(
                {
                    "harvest_batch_id": str(batch.id),
                    "match_score": match_score,
                    "reason": "Same crop and grade, acceptable price, and operationally feasible distance",
                }
            )

        matches.sort(key=lambda item: item["match_score"], reverse=True)
        return {"buyer_demand_id": str(demand.id), "matches": matches}
