from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import require_permission
from app.models.buyer_demand import BuyerDemand
from app.models.enums import BuyerDemandStatus, HarvestBatchStatus
from app.models.harvest_batch import HarvestBatch
from app.schemas.matching import MatchRequest
from app.services.buyer_demand_service import BuyerDemandService
from app.services.matching_service import MatchingService
from app.utils.response import success_response

router = APIRouter(prefix="/matching", tags=["Matching"])


@router.post("/harvest-to-demand")
def harvest_to_demand(payload: MatchRequest, db: Session = Depends(get_db), _=Depends(require_permission("matching:write"))):
    demand = BuyerDemandService(db).get(payload.buyer_demand_id)
    data = MatchingService(db).match_harvest_to_demand(demand)
    return success_response("Operation completed successfully", data)


@router.post("/route-cluster")
def route_cluster(payload: dict, db: Session = Depends(get_db), _=Depends(require_permission("matching:write"))):
    demand = BuyerDemandService(db).get(payload["buyer_demand_id"])
    data = MatchingService(db).match_harvest_to_demand(demand)
    return success_response("Operation completed successfully", {"clustered_matches": data["matches"]})


@router.get("/recommendations")
def recommendations(db: Session = Depends(get_db), _=Depends(require_permission("matching:read"))):
    demand = db.query(BuyerDemand).filter(BuyerDemand.status == BuyerDemandStatus.OPEN).first()
    if not demand:
        return success_response("Records retrieved successfully", {"matches": []})
    data = MatchingService(db).match_harvest_to_demand(demand)
    return success_response("Records retrieved successfully", data)


@router.get("/unmatched-harvests")
def unmatched_harvests(db: Session = Depends(get_db), _=Depends(require_permission("matching:read"))):
    rows = db.query(HarvestBatch).filter(HarvestBatch.status.in_([HarvestBatchStatus.DRAFT, HarvestBatchStatus.READY])).all()
    return success_response(
        "Records retrieved successfully",
        [{"id": str(item.id), "crop_id": str(item.crop_id), "quantity_kg": item.quantity_kg} for item in rows],
    )


@router.get("/unfulfilled-demands")
def unfulfilled_demands(db: Session = Depends(get_db), _=Depends(require_permission("matching:read"))):
    rows = db.query(BuyerDemand).filter(BuyerDemand.status == BuyerDemandStatus.OPEN).all()
    return success_response(
        "Records retrieved successfully",
        [{"id": str(item.id), "crop_id": str(item.crop_id), "quantity_kg": item.quantity_kg} for item in rows],
    )
