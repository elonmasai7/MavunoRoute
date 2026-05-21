from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import audit_action, enforce_owner_or_privileged, get_current_user, require_permission
from app.models.transporter import TransporterProfile
from app.models.vehicle import Vehicle
from app.schemas.vehicles import VehicleAvailabilityUpdate, VehicleCreate, VehicleRead, VehicleUpdate
from app.services.vehicle_service import VehicleService
from app.utils.pagination import build_pagination_meta
from app.utils.response import success_response

router = APIRouter(prefix="/vehicles", tags=["Vehicles"])


@router.post("")
def create_vehicle(
    payload: VehicleCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    _=Depends(require_permission("vehicles:write")),
    __=Depends(audit_action("VEHICLE_CREATE", "VEHICLE")),
):
    transporter = db.get(TransporterProfile, payload.transporter_id)
    if transporter and current_user.role == "TRANSPORTER":
        enforce_owner_or_privileged(current_user, transporter.user_id)
    vehicle = VehicleService(db).create(payload)
    return success_response("Operation completed successfully", VehicleRead.model_validate(vehicle).model_dump(mode="json"))


@router.get("")
def list_vehicles(
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    _=Depends(require_permission("vehicles:read")),
):
    if current_user.role == "TRANSPORTER":
        transporter = db.query(TransporterProfile).filter(TransporterProfile.user_id == current_user.id).first()
        if not transporter:
            return success_response("Records retrieved successfully", [], build_pagination_meta(page, per_page, 0))
        query = db.query(Vehicle).filter(Vehicle.transporter_id == transporter.id)
        total = query.count()
        rows = query.offset((page - 1) * per_page).limit(per_page).all()
    else:
        rows, total = VehicleService(db).list(page, per_page)
    data = [VehicleRead.model_validate(item).model_dump(mode="json") for item in rows]
    return success_response("Records retrieved successfully", data, build_pagination_meta(page, per_page, total))


@router.get("/available")
def available_vehicles(
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    _=Depends(require_permission("vehicles:read")),
):
    rows, total = VehicleService(db).available(page, per_page)
    data = [VehicleRead.model_validate(item).model_dump(mode="json") for item in rows]
    return success_response("Records retrieved successfully", data, build_pagination_meta(page, per_page, total))


@router.get("/{vehicle_id}")
def get_vehicle(
    vehicle_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    _=Depends(require_permission("vehicles:read")),
):
    vehicle = VehicleService(db).get(vehicle_id)
    if current_user.role == "TRANSPORTER":
        transporter = db.get(TransporterProfile, vehicle.transporter_id)
        if transporter:
            enforce_owner_or_privileged(current_user, transporter.user_id)
    return success_response("Record retrieved successfully", VehicleRead.model_validate(vehicle).model_dump(mode="json"))


@router.patch("/{vehicle_id}")
def update_vehicle(
    vehicle_id: UUID,
    payload: VehicleUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    _=Depends(require_permission("vehicles:write")),
    __=Depends(audit_action("VEHICLE_UPDATE", "VEHICLE")),
):
    current = VehicleService(db).get(vehicle_id)
    if current_user.role == "TRANSPORTER":
        transporter = db.get(TransporterProfile, current.transporter_id)
        if transporter:
            enforce_owner_or_privileged(current_user, transporter.user_id)
    vehicle = VehicleService(db).update(vehicle_id, payload)
    return success_response("Record updated successfully", VehicleRead.model_validate(vehicle).model_dump(mode="json"))


@router.patch("/{vehicle_id}/availability")
def update_vehicle_availability(
    vehicle_id: UUID,
    payload: VehicleAvailabilityUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    _=Depends(require_permission("vehicles:write")),
    __=Depends(audit_action("VEHICLE_AVAILABILITY_UPDATE", "VEHICLE")),
):
    current = VehicleService(db).get(vehicle_id)
    if current_user.role == "TRANSPORTER":
        transporter = db.get(TransporterProfile, current.transporter_id)
        if transporter:
            enforce_owner_or_privileged(current_user, transporter.user_id)
    vehicle = VehicleService(db).set_availability(vehicle_id, payload.is_available)
    return success_response("Operation completed successfully", VehicleRead.model_validate(vehicle).model_dump(mode="json"))
