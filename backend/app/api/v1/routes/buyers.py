from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import audit_action, enforce_owner_or_privileged, get_current_user, require_permission
from app.models.buyer import BuyerProfile
from app.models.buyer_demand import BuyerDemand
from app.models.payment import Payment
from app.schemas.buyers import BuyerCreate, BuyerRead, BuyerUpdate
from app.services.buyer_service import BuyerService
from app.utils.pagination import build_pagination_meta
from app.utils.response import success_response

router = APIRouter(prefix="/buyers", tags=["Buyers"])


@router.post("")
def create_buyer(
    payload: BuyerCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    _=Depends(require_permission("buyers:write")),
    __=Depends(audit_action("BUYER_CREATE", "BUYER")),
):
    if current_user.role == "BUYER":
        enforce_owner_or_privileged(current_user, payload.user_id)
    buyer = BuyerService(db).create(payload)
    return success_response("Operation completed successfully", BuyerRead.model_validate(buyer).model_dump(mode="json"))


@router.get("")
def list_buyers(
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    _=Depends(require_permission("buyers:read")),
):
    if current_user.role == "BUYER":
        query = db.query(BuyerProfile).filter(BuyerProfile.user_id == current_user.id)
        total = query.count()
        rows = query.offset((page - 1) * per_page).limit(per_page).all()
    else:
        rows, total = BuyerService(db).list(page, per_page)
    data = [BuyerRead.model_validate(item).model_dump(mode="json") for item in rows]
    return success_response("Records retrieved successfully", data, build_pagination_meta(page, per_page, total))


@router.get("/{buyer_id}")
def get_buyer(
    buyer_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    _=Depends(require_permission("buyers:read")),
):
    buyer = BuyerService(db).get(buyer_id)
    if current_user.role == "BUYER":
        enforce_owner_or_privileged(current_user, buyer.user_id)
    return success_response("Record retrieved successfully", BuyerRead.model_validate(buyer).model_dump(mode="json"))


@router.patch("/{buyer_id}")
def update_buyer(
    buyer_id: UUID,
    payload: BuyerUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    _=Depends(require_permission("buyers:write")),
    __=Depends(audit_action("BUYER_UPDATE", "BUYER")),
):
    existing = BuyerService(db).get(buyer_id)
    if current_user.role == "BUYER":
        enforce_owner_or_privileged(current_user, existing.user_id)
    buyer = BuyerService(db).update(buyer_id, payload.model_dump(exclude_unset=True))
    return success_response("Record updated successfully", BuyerRead.model_validate(buyer).model_dump(mode="json"))


@router.get("/{buyer_id}/demands")
def buyer_demands(
    buyer_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    _=Depends(require_permission("demands:read")),
):
    buyer = BuyerService(db).get(buyer_id)
    if current_user.role == "BUYER":
        enforce_owner_or_privileged(current_user, buyer.user_id)
    rows = db.query(BuyerDemand).filter(BuyerDemand.buyer_id == buyer_id).all()
    return success_response(
        "Records retrieved successfully",
        [{"id": str(item.id), "status": item.status, "quantity_kg": item.quantity_kg} for item in rows],
    )


@router.get("/{buyer_id}/orders")
def buyer_orders(
    buyer_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    _=Depends(require_permission("demands:read")),
):
    buyer = BuyerService(db).get(buyer_id)
    if current_user.role == "BUYER":
        enforce_owner_or_privileged(current_user, buyer.user_id)
    rows = db.query(BuyerDemand).filter(BuyerDemand.buyer_id == buyer_id).all()
    return success_response(
        "Records retrieved successfully",
        [{"id": str(item.id), "status": item.status, "required_delivery_datetime": item.required_delivery_datetime} for item in rows],
    )


@router.get("/{buyer_id}/payments")
def buyer_payments(
    buyer_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    _=Depends(require_permission("payments:read")),
):
    buyer = db.get(BuyerProfile, buyer_id)
    if not buyer:
        return success_response("Record not found", {})
    if current_user.role == "BUYER":
        enforce_owner_or_privileged(current_user, buyer.user_id)
    total = float(db.query(func.coalesce(func.sum(Payment.amount), 0)).filter(Payment.payer_user_id == buyer.user_id).scalar() or 0)
    return success_response("Records retrieved successfully", {"buyer_id": str(buyer_id), "total_payments": total, "currency": "KES"})
