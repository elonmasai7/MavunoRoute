from datetime import UTC, datetime
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.route_stop import RouteStop


class RouteStopService:
    def __init__(self, db: Session):
        self.db = db

    def get(self, stop_id: UUID):
        stop = self.db.get(RouteStop, stop_id)
        if not stop:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Route stop not found")
        return stop

    def arrive(self, stop_id: UUID):
        stop = self.get(stop_id)
        stop.actual_arrival_time = datetime.now(UTC)
        stop.status = "ARRIVED"
        self.db.commit()
        self.db.refresh(stop)
        return stop

    def complete(self, stop_id: UUID):
        stop = self.get(stop_id)
        stop.status = "COMPLETED"
        if stop.actual_arrival_time is None:
            stop.actual_arrival_time = datetime.now(UTC)
        self.db.commit()
        self.db.refresh(stop)
        return stop

    def skip(self, stop_id: UUID):
        stop = self.get(stop_id)
        stop.status = "SKIPPED"
        self.db.commit()
        self.db.refresh(stop)
        return stop
