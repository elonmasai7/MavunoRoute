from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import audit_action, require_permission
from app.models.temperature_event import TemperatureEvent
from app.schemas.temperature_events import TemperatureEventCreate
from app.services.temperature_event_service import TemperatureEventService
from app.utils.pagination import build_pagination_meta
from app.utils.response import success_response

router = APIRouter(prefix="/temperature-events", tags=["Temperature Events"])


@router.post("")
def create_temperature_event(
    payload: TemperatureEventCreate,
    db: Session = Depends(get_db),
    _=Depends(require_permission("temperature:write")),
    __=Depends(audit_action("TEMPERATURE_EVENT_CREATE", "TEMPERATURE_EVENT")),
):
    event = TemperatureEventService(db).create(payload)
    return success_response("Operation completed successfully", {"id": str(event.id)})


@router.get("")
def list_temperature_events(
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    _=Depends(require_permission("temperature:read")),
):
    rows, total = TemperatureEventService(db).list(page, per_page)
    data = [
        {
            "id": str(item.id),
            "harvest_batch_id": str(item.harvest_batch_id),
            "temperature_celsius": item.temperature_celsius,
            "recorded_at": item.recorded_at,
        }
        for item in rows
    ]
    return success_response("Records retrieved successfully", data, build_pagination_meta(page, per_page, total))


@router.get("/{event_id}")
def get_temperature_event(event_id: UUID, db: Session = Depends(get_db), _=Depends(require_permission("temperature:read"))):
    event = TemperatureEventService(db).get(event_id)
    return success_response(
        "Record retrieved successfully",
        {
            "id": str(event.id),
            "harvest_batch_id": str(event.harvest_batch_id),
            "temperature_celsius": event.temperature_celsius,
            "recorded_at": event.recorded_at,
        },
    )


@router.get("/harvest-batch/{batch_id}")
def get_temperature_for_batch(batch_id: UUID, db: Session = Depends(get_db), _=Depends(require_permission("temperature:read"))):
    rows = db.query(TemperatureEvent).filter(TemperatureEvent.harvest_batch_id == batch_id).all()
    return success_response(
        "Records retrieved successfully",
        [{"id": str(item.id), "temperature_celsius": item.temperature_celsius, "recorded_at": item.recorded_at} for item in rows],
    )


@router.get("/transport-job/{job_id}")
def get_temperature_for_job(job_id: UUID, db: Session = Depends(get_db), _=Depends(require_permission("temperature:read"))):
    rows = db.query(TemperatureEvent).filter(TemperatureEvent.transport_job_id == job_id).all()
    return success_response(
        "Records retrieved successfully",
        [{"id": str(item.id), "temperature_celsius": item.temperature_celsius, "recorded_at": item.recorded_at} for item in rows],
    )
