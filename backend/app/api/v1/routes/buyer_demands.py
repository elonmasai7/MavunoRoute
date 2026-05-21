from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import audit_action, enforce_owner_or_privileged, get_current_user, require_permission
from app.models.buyer import BuyerProfile
from app.models.buyer_demand import BuyerDemand
from app.schemas.buyer_demands import BuyerDemandCreate, BuyerDemandRead, BuyerDemandUpdate
from app.services.buyer_demand_service import BuyerDemandService
from app.services.matching_service import MatchingService
from app.utils.pagination import build_pagination_meta
from app.utils.response import success_response

router = APIRouter(prefix="/buyer-demands", tags=["Buyer Demands"])


@router.post("")
def create_buyer_demand(
    payload: BuyerDemandCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    _=Depends(require_permission("demands:write")),
    __=Depends(audit_action("DEMAND_CREATE", "BUYER_DEMAND")),
):
    buyer = db.get(BuyerProfile, payload.buyer_id)
    if buyer and current_user.role == "BUYER":
        enforce_owner_or_privileged(current_user, buyer.user_id)
    demand = BuyerDemandService(db).create(payload)
    return success_response("Operation completed successfully", BuyerDemandRead.model_validate(demand).model_dump(mode="json"))


@router.get("")
def list_buyer_demands(
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    _=Depends(require_permission("demands:read")),
):
    if current_user.role == "BUYER":
        buyer = db.query(BuyerProfile).filter(BuyerProfile.user_id == current_user.id).first()
        if not buyer:
            return success_response("Records retrieved successfully", [], build_pagination_meta(page, per_page, 0))
        query = db.query(BuyerDemand).filter(BuyerDemand.buyer_id == buyer.id)
        total = query.count()
        rows = query.offset((page - 1) * per_page).limit(per_page).all()
    else:
        rows, total = BuyerDemandService(db).list(page, per_page)
    data = [BuyerDemandRead.model_validate(item).model_dump(mode="json") for item in rows]
    return success_response("Records retrieved successfully", data, build_pagination_meta(page, per_page, total))


@router.get("/{demand_id}")
def get_buyer_demand(
    demand_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    _=Depends(require_permission("demands:read")),
):
    demand = BuyerDemandService(db).get(demand_id)
    if current_user.role == "BUYER":
        buyer = db.get(BuyerProfile, demand.buyer_id)
        if buyer:
            enforce_owner_or_privileged(current_user, buyer.user_id)
    return success_response("Record retrieved successfully", BuyerDemandRead.model_validate(demand).model_dump(mode="json"))


@router.patch("/{demand_id}")
def update_buyer_demand(
    demand_id: UUID,
    payload: BuyerDemandUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    _=Depends(require_permission("demands:write")),
    __=Depends(audit_action("DEMAND_UPDATE", "BUYER_DEMAND")),
):
    current = BuyerDemandService(db).get(demand_id)
    if current_user.role == "BUYER":
        buyer = db.get(BuyerProfile, current.buyer_id)
        if buyer:
            enforce_owner_or_privileged(current_user, buyer.user_id)
    demand = BuyerDemandService(db).update(demand_id, payload)
    return success_response("Record updated successfully", BuyerDemandRead.model_validate(demand).model_dump(mode="json"))


@router.post("/{demand_id}/match-harvests")
def match_harvests(
    demand_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    _=Depends(require_permission("matching:write")),
):
    demand = BuyerDemandService(db).get(demand_id)
    if current_user.role == "BUYER":
        buyer = db.get(BuyerProfile, demand.buyer_id)
        if buyer:
            enforce_owner_or_privileged(current_user, buyer.user_id)
    matches = MatchingService(db).match_harvest_to_demand(demand)
    return success_response("Operation completed successfully", matches)


@router.patch("/{demand_id}/status")
def update_buyer_demand_status(
    demand_id: UUID,
    payload: dict,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    _=Depends(require_permission("demands:write")),
    __=Depends(audit_action("DEMAND_STATUS_UPDATE", "BUYER_DEMAND")),
):
    current = BuyerDemandService(db).get(demand_id)
    if current_user.role == "BUYER":
        buyer = db.get(BuyerProfile, current.buyer_id)
        if buyer:
            enforce_owner_or_privileged(current_user, buyer.user_id)
    demand = BuyerDemandService(db).update(demand_id, BuyerDemandUpdate(status=payload["status"]))
    return success_response("Operation completed successfully", BuyerDemandRead.model_validate(demand).model_dump(mode="json"))


@router.get("/{demand_id}/matches")
def get_buyer_demand_matches(
    demand_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    _=Depends(require_permission("matching:read")),
):
    demand = BuyerDemandService(db).get(demand_id)
    if current_user.role == "BUYER":
        buyer = db.get(BuyerProfile, demand.buyer_id)
        if buyer:
            enforce_owner_or_privileged(current_user, buyer.user_id)
    data = MatchingService(db).match_harvest_to_demand(demand)
    return success_response("Records retrieved successfully", data)
