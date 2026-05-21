from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import audit_action, enforce_owner_or_privileged, get_current_user, require_permission
from app.models.enums import HarvestBatchStatus
from app.models.farmer import FarmerProfile
from app.models.harvest_batch import HarvestBatch
from app.models.payment import Payment
from app.schemas.farmers import FarmerCreate, FarmerRead, FarmerUpdate
from app.services.farmer_service import FarmerService
from app.utils.pagination import build_pagination_meta
from app.utils.response import success_response

router = APIRouter(prefix="/farmers", tags=["Farmers"])


@router.post("")
def create_farmer(
    payload: FarmerCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    _=Depends(require_permission("farmers:write")),
    __=Depends(audit_action("FARMER_CREATE", "FARMER")),
):
    if current_user.role == "FARMER":
        enforce_owner_or_privileged(current_user, payload.user_id)
    farmer = FarmerService(db).create(payload)
    return success_response("Operation completed successfully", FarmerRead.model_validate(farmer).model_dump(mode="json"))


@router.get("")
def list_farmers(
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    _=Depends(require_permission("farmers:read")),
):
    if current_user.role == "FARMER":
        query = db.query(FarmerProfile).filter(FarmerProfile.user_id == current_user.id)
        total = query.count()
        rows = query.offset((page - 1) * per_page).limit(per_page).all()
    else:
        rows, total = FarmerService(db).list(page, per_page)
    data = [FarmerRead.model_validate(item).model_dump(mode="json") for item in rows]
    return success_response("Records retrieved successfully", data, build_pagination_meta(page, per_page, total))


@router.get("/{farmer_id}")
def get_farmer(
    farmer_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    _=Depends(require_permission("farmers:read")),
):
    farmer = FarmerService(db).get(farmer_id)
    if current_user.role == "FARMER":
        enforce_owner_or_privileged(current_user, farmer.user_id)
    return success_response("Record retrieved successfully", FarmerRead.model_validate(farmer).model_dump(mode="json"))


@router.patch("/{farmer_id}")
def update_farmer(
    farmer_id: UUID,
    payload: FarmerUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    _=Depends(require_permission("farmers:write")),
    __=Depends(audit_action("FARMER_UPDATE", "FARMER")),
):
    existing = FarmerService(db).get(farmer_id)
    if current_user.role == "FARMER":
        enforce_owner_or_privileged(current_user, existing.user_id)
    farmer = FarmerService(db).update(farmer_id, payload)
    return success_response("Record updated successfully", FarmerRead.model_validate(farmer).model_dump(mode="json"))


@router.get("/{farmer_id}/harvests")
def farmer_harvests(
    farmer_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    _=Depends(require_permission("harvests:read")),
):
    farmer = FarmerService(db).get(farmer_id)
    if current_user.role == "FARMER":
        enforce_owner_or_privileged(current_user, farmer.user_id)
    rows = db.query(HarvestBatch).filter(HarvestBatch.farmer_id == farmer_id).all()
    return success_response(
        "Records retrieved successfully",
        [{"id": str(item.id), "crop_id": str(item.crop_id), "quantity_kg": item.quantity_kg, "status": item.status} for item in rows],
    )


@router.get("/{farmer_id}/payments")
def farmer_payments(
    farmer_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    _=Depends(require_permission("payments:read")),
):
    farmer = FarmerService(db).get(farmer_id)
    if current_user.role == "FARMER":
        enforce_owner_or_privileged(current_user, farmer.user_id)
    total = float(db.query(func.coalesce(func.sum(Payment.amount), 0)).filter(Payment.payee_user_id == farmer.user_id).scalar() or 0)
    return success_response("Records retrieved successfully", {"farmer_id": str(farmer_id), "total_payments": total, "currency": "KES"})


@router.get("/{farmer_id}/performance")
def farmer_performance(
    farmer_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    _=Depends(require_permission("reports:read")),
):
    farmer = FarmerService(db).get(farmer_id)
    if current_user.role == "FARMER":
        enforce_owner_or_privileged(current_user, farmer.user_id)
    total_batches = db.query(HarvestBatch).filter(HarvestBatch.farmer_id == farmer_id).count()
    delivered = db.query(HarvestBatch).filter(
        HarvestBatch.farmer_id == farmer_id, HarvestBatch.status == HarvestBatchStatus.DELIVERED
    ).count()
    return success_response(
        "Records retrieved successfully",
        {"farmer_id": str(farmer_id), "total_batches": total_batches, "delivered_batches": delivered},
    )
