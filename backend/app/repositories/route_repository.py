from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.route_plan import RoutePlan
from app.models.route_stop import RouteStop
from app.models.transport_job import TransportJob


class RouteRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_route(self, route: RoutePlan) -> RoutePlan:
        self.db.add(route)
        self.db.flush()
        self.db.refresh(route)
        return route

    def create_stops(self, stops: list[RouteStop]) -> list[RouteStop]:
        self.db.add_all(stops)
        self.db.flush()
        return stops

    def create_jobs(self, jobs: list[TransportJob]) -> list[TransportJob]:
        self.db.add_all(jobs)
        self.db.flush()
        return jobs

    def get_route(self, route_id: UUID) -> RoutePlan | None:
        return self.db.get(RoutePlan, route_id)

    def list_routes(self, page: int, per_page: int) -> tuple[list[RoutePlan], int]:
        stmt = select(RoutePlan).offset((page - 1) * per_page).limit(per_page)
        rows = self.db.scalars(stmt).all()
        total = self.db.query(RoutePlan).count()
        return rows, total
