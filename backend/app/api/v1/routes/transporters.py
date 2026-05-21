from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import audit_action, enforce_owner_or_privileged, get_current_user, require_permission
from app.models.transporter import TransporterProfile
from app.schemas.transporters import TransporterCreate, TransporterRead, TransporterUpdate
from app.services.transporter_service import TransporterService
from app.utils.pagination import build_pagination_meta
from app.utils.response import success_response

router = APIRouter(prefix="/transporters", tags=["Transporters"])


@router.post("")
def create_transporter(
    payload: TransporterCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    _=Depends(require_permission("transporters:write")),
    __=Depends(audit_action("TRANSPORTER_CREATE", "TRANSPORTER")),
):
    if current_user.role == "TRANSPORTER":
        enforce_owner_or_privileged(current_user, payload.user_id)
    item = TransporterService(db).create(payload)
    return success_response("Operation completed successfully", TransporterRead.model_validate(item).model_dump(mode="json"))


@router.get("")
def list_transporters(
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    _=Depends(require_permission("transporters:read")),
):
    if current_user.role == "TRANSPORTER":
        query = db.query(TransporterProfile).filter(TransporterProfile.user_id == current_user.id)
        total = query.count()
        rows = query.offset((page - 1) * per_page).limit(per_page).all()
    else:
        rows, total = TransporterService(db).list(page, per_page)
    data = [TransporterRead.model_validate(item).model_dump(mode="json") for item in rows]
    return success_response("Records retrieved successfully", data, build_pagination_meta(page, per_page, total))


@router.get("/{transporter_id}")
def get_transporter(
    transporter_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    _=Depends(require_permission("transporters:read")),
):
    item = TransporterService(db).get(transporter_id)
    if current_user.role == "TRANSPORTER":
        enforce_owner_or_privileged(current_user, item.user_id)
    return success_response("Record retrieved successfully", TransporterRead.model_validate(item).model_dump(mode="json"))


@router.patch("/{transporter_id}")
def update_transporter(
    transporter_id: UUID,
    payload: TransporterUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    _=Depends(require_permission("transporters:write")),
    __=Depends(audit_action("TRANSPORTER_UPDATE", "TRANSPORTER")),
):
    existing = TransporterService(db).get(transporter_id)
    if current_user.role == "TRANSPORTER":
        enforce_owner_or_privileged(current_user, existing.user_id)
    item = TransporterService(db).update(transporter_id, payload)
    return success_response("Record updated successfully", TransporterRead.model_validate(item).model_dump(mode="json"))


@router.get("/{transporter_id}/vehicles")
def transporter_vehicles(
    transporter_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    _=Depends(require_permission("vehicles:read")),
):
    existing = TransporterService(db).get(transporter_id)
    if current_user.role == "TRANSPORTER":
        enforce_owner_or_privileged(current_user, existing.user_id)
    rows = TransporterService(db).vehicles(transporter_id)
    return success_response(
        "Records retrieved successfully",
        [{"id": str(item.id), "plate_number": item.plate_number, "is_available": item.is_available} for item in rows],
    )


@router.get("/{transporter_id}/jobs")
def transporter_jobs(
    transporter_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    _=Depends(require_permission("jobs:read")),
):
    existing = TransporterService(db).get(transporter_id)
    if current_user.role == "TRANSPORTER":
        enforce_owner_or_privileged(current_user, existing.user_id)
    rows = TransporterService(db).jobs(transporter_id)
    return success_response(
        "Records retrieved successfully",
        [
            {
                "id": str(item.id),
                "route_plan_id": str(item.route_plan_id),
                "pickup_status": item.pickup_status,
                "delivery_status": item.delivery_status,
            }
            for item in rows
        ],
    )


@router.get("/{transporter_id}/earnings")
def transporter_earnings(
    transporter_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    _=Depends(require_permission("payments:read")),
):
    existing = TransporterService(db).get(transporter_id)
    if current_user.role == "TRANSPORTER":
        enforce_owner_or_privileged(current_user, existing.user_id)
    return success_response("Records retrieved successfully", TransporterService(db).earnings(transporter_id))
