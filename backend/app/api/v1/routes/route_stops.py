from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import audit_action, require_permission
from app.services.route_stop_service import RouteStopService
from app.utils.response import success_response

router = APIRouter(prefix="/route-stops", tags=["Route Stops"])


@router.get("/{stop_id}")
def get_route_stop(stop_id: UUID, db: Session = Depends(get_db), _=Depends(require_permission("routes:read"))):
    stop = RouteStopService(db).get(stop_id)
    return success_response(
        "Record retrieved successfully",
        {
            "id": str(stop.id),
            "route_plan_id": str(stop.route_plan_id),
            "status": stop.status,
            "sequence_number": stop.sequence_number,
        },
    )


@router.patch("/{stop_id}/arrive")
def arrive(
    stop_id: UUID,
    db: Session = Depends(get_db),
    _=Depends(require_permission("routes:write")),
    __=Depends(audit_action("ROUTE_STOP_ARRIVE", "ROUTE_STOP")),
):
    stop = RouteStopService(db).arrive(stop_id)
    return success_response("Operation completed successfully", {"id": str(stop.id), "status": stop.status})


@router.patch("/{stop_id}/complete")
def complete(
    stop_id: UUID,
    db: Session = Depends(get_db),
    _=Depends(require_permission("routes:write")),
    __=Depends(audit_action("ROUTE_STOP_COMPLETE", "ROUTE_STOP")),
):
    stop = RouteStopService(db).complete(stop_id)
    return success_response("Operation completed successfully", {"id": str(stop.id), "status": stop.status})


@router.patch("/{stop_id}/skip")
def skip(
    stop_id: UUID,
    db: Session = Depends(get_db),
    _=Depends(require_permission("routes:write")),
    __=Depends(audit_action("ROUTE_STOP_SKIP", "ROUTE_STOP")),
):
    stop = RouteStopService(db).skip(stop_id)
    return success_response("Operation completed successfully", {"id": str(stop.id), "status": stop.status})
