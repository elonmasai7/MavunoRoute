from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import audit_action, enforce_owner_or_privileged, get_current_user, require_permission
from app.models.transporter import TransporterProfile
from app.models.transport_job import TransportJob
from app.schemas.transport_jobs import TransportJobCreate, TransportJobRead, TransportJobUpdate
from app.services.transport_job_service import TransportJobService
from app.utils.pagination import build_pagination_meta
from app.utils.response import success_response

router = APIRouter(prefix="/transport-jobs", tags=["Transport Jobs"])


@router.post("")
def create_job(
    payload: TransportJobCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    _=Depends(require_permission("jobs:write")),
    __=Depends(audit_action("JOB_CREATE", "TRANSPORT_JOB")),
):
    if current_user.role == "TRANSPORTER":
        transporter = db.get(TransporterProfile, payload.transporter_id)
        if not transporter:
            raise HTTPException(status_code=404, detail="Transporter profile not found")
        enforce_owner_or_privileged(current_user, transporter.user_id)
    job = TransportJobService(db).create(payload)
    return success_response("Operation completed successfully", TransportJobRead.model_validate(job).model_dump(mode="json"))


@router.get("")
def list_jobs(
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    _=Depends(require_permission("jobs:read")),
):
    if current_user.role == "TRANSPORTER":
        transporter = db.query(TransporterProfile).filter(TransporterProfile.user_id == current_user.id).first()
        if not transporter:
            return success_response("Records retrieved successfully", [], build_pagination_meta(page, per_page, 0))
        query = db.query(TransportJob).filter(TransportJob.transporter_id == transporter.id)
        total = query.count()
        rows = query.offset((page - 1) * per_page).limit(per_page).all()
    else:
        rows, total = TransportJobService(db).list(page, per_page)
    data = [TransportJobRead.model_validate(item).model_dump(mode="json") for item in rows]
    return success_response("Records retrieved successfully", data, build_pagination_meta(page, per_page, total))


@router.get("/{job_id}")
def get_job(
    job_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    _=Depends(require_permission("jobs:read")),
):
    job = TransportJobService(db).get(job_id)
    if current_user.role == "TRANSPORTER":
        transporter = db.get(TransporterProfile, job.transporter_id)
        if transporter:
            enforce_owner_or_privileged(current_user, transporter.user_id)
    return success_response("Record retrieved successfully", TransportJobRead.model_validate(job).model_dump(mode="json"))


@router.patch("/{job_id}")
def update_job(
    job_id: UUID,
    payload: TransportJobUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    _=Depends(require_permission("jobs:write")),
    __=Depends(audit_action("JOB_UPDATE", "TRANSPORT_JOB")),
):
    existing = TransportJobService(db).get(job_id)
    if current_user.role == "TRANSPORTER":
        transporter = db.get(TransporterProfile, existing.transporter_id)
        if transporter:
            enforce_owner_or_privileged(current_user, transporter.user_id)
    job = TransportJobService(db).update(job_id, payload)
    return success_response("Record updated successfully", TransportJobRead.model_validate(job).model_dump(mode="json"))


@router.patch("/{job_id}/accept")
def accept_job(
    job_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    _=Depends(require_permission("jobs:write")),
    __=Depends(audit_action("JOB_ACCEPT", "TRANSPORT_JOB")),
):
    existing = TransportJobService(db).get(job_id)
    if current_user.role == "TRANSPORTER":
        transporter = db.get(TransporterProfile, existing.transporter_id)
        if transporter:
            enforce_owner_or_privileged(current_user, transporter.user_id)
    job = TransportJobService(db).accept(job_id)
    return success_response("Operation completed successfully", TransportJobRead.model_validate(job).model_dump(mode="json"))


@router.patch("/{job_id}/pickup")
def pickup_job(
    job_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    _=Depends(require_permission("jobs:write")),
    __=Depends(audit_action("JOB_PICKUP", "TRANSPORT_JOB")),
):
    existing = TransportJobService(db).get(job_id)
    if current_user.role == "TRANSPORTER":
        transporter = db.get(TransporterProfile, existing.transporter_id)
        if transporter:
            enforce_owner_or_privileged(current_user, transporter.user_id)
    job = TransportJobService(db).mark_pickup(job_id)
    return success_response("Operation completed successfully", TransportJobRead.model_validate(job).model_dump(mode="json"))


@router.patch("/{job_id}/deliver")
def deliver_job(
    job_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    _=Depends(require_permission("jobs:write")),
    __=Depends(audit_action("JOB_DELIVER", "TRANSPORT_JOB")),
):
    existing = TransportJobService(db).get(job_id)
    if current_user.role == "TRANSPORTER":
        transporter = db.get(TransporterProfile, existing.transporter_id)
        if transporter:
            enforce_owner_or_privileged(current_user, transporter.user_id)
    job = TransportJobService(db).mark_delivery(job_id)
    return success_response("Operation completed successfully", TransportJobRead.model_validate(job).model_dump(mode="json"))


@router.patch("/{job_id}/reject")
def reject_job(
    job_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    _=Depends(require_permission("jobs:write")),
    __=Depends(audit_action("JOB_REJECT", "TRANSPORT_JOB")),
):
    existing = TransportJobService(db).get(job_id)
    if current_user.role == "TRANSPORTER":
        transporter = db.get(TransporterProfile, existing.transporter_id)
        if transporter:
            enforce_owner_or_privileged(current_user, transporter.user_id)
    job = TransportJobService(db).reject(job_id)
    return success_response("Operation completed successfully", TransportJobRead.model_validate(job).model_dump(mode="json"))


@router.patch("/{job_id}/cancel")
def cancel_job(
    job_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    _=Depends(require_permission("jobs:write")),
    __=Depends(audit_action("JOB_CANCEL", "TRANSPORT_JOB")),
):
    existing = TransportJobService(db).get(job_id)
    if current_user.role == "TRANSPORTER":
        transporter = db.get(TransporterProfile, existing.transporter_id)
        if transporter:
            enforce_owner_or_privileged(current_user, transporter.user_id)
    job = TransportJobService(db).cancel(job_id)
    return success_response("Operation completed successfully", TransportJobRead.model_validate(job).model_dump(mode="json"))
