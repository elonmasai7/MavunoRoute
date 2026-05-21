from datetime import UTC, datetime, timedelta

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.models.buyer import BuyerProfile
from app.models.cold_hub import ColdHub
from app.models.harvest_batch import HarvestBatch
from app.models.route_plan import RoutePlan
from app.models.route_stop import RouteStop
from app.models.enums import RouteStatus
from app.models.transport_job import TransportJob
from app.models.vehicle import Vehicle
from app.providers.routing.osrm_provider import OSRMRoutingProvider
from app.repositories.route_repository import RouteRepository
from app.schemas.routes import RoutePlanCreate

settings = get_settings()


class RouteOptimizationService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = RouteRepository(db)

        if settings.routing_provider.lower() == "osrm" and settings.osrm_base_url:
            self.provider = OSRMRoutingProvider(settings.osrm_base_url)
        else:
            self.provider = None

    async def plan_route(self, payload: RoutePlanCreate) -> dict:
        if self.provider is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Routing provider not configured",
            )

        batches = self.db.scalars(select(HarvestBatch).where(HarvestBatch.id.in_(payload.harvest_batch_ids))).all()
        if len(batches) != len(payload.harvest_batch_ids):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="One or more harvest batches are missing")

        total_kg = sum(batch.quantity_kg for batch in batches)
        if not payload.vehicle_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Vehicle assignment is required")

        selected_vehicle = self.db.get(Vehicle, payload.vehicle_id)
        if not selected_vehicle:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found")
        if selected_vehicle.capacity_kg < total_kg:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Vehicle capacity is insufficient")

        destination = None
        destination_type = None
        if payload.destination_buyer_id:
            destination = self.db.get(BuyerProfile, payload.destination_buyer_id)
            destination_type = "BUYER"
        elif payload.destination_cold_hub_id:
            destination = self.db.get(ColdHub, payload.destination_cold_hub_id)
            destination_type = "COLD_HUB"

        if destination is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Destination buyer or cold hub is required")

        points = [(batch.latitude, batch.longitude) for batch in batches]
        points.append((destination.latitude, destination.longitude))

        ordered_indexes = await self.provider.optimize_stops(points)
        ordered_points = [points[idx] for idx in ordered_indexes]
        distance_matrix = await self.provider.get_distance_matrix(ordered_points)
        duration = await self.provider.estimate_duration(ordered_points)
        polyline = await self.provider.get_route_polyline(ordered_points)
        total_distance = sum(distance_matrix[i][i + 1] for i in range(len(distance_matrix) - 1)) / 1000 if distance_matrix else 0

        route = RoutePlan(
            route_code=f"MR-{datetime.now(UTC).strftime('%Y%m%d%H%M%S')}",
            origin_county="MULTI",
            destination_county=getattr(destination, "county", "UNKNOWN"),
            vehicle_id=getattr(selected_vehicle, "id", None),
            transporter_id=getattr(selected_vehicle, "transporter_id", None),
            assigned_driver_id=None,
            total_distance_km=round(total_distance, 2),
            estimated_duration_minutes=duration,
            route_polyline=polyline,
            route_provider=settings.routing_provider,
        )
        self.repo.create_route(route)

        stops = []
        now = datetime.now(UTC)
        for idx, point in enumerate(ordered_points, start=1):
            if idx <= len(batches):
                batch = batches[idx - 1]
                stops.append(
                    RouteStop(
                        route_plan_id=route.id,
                        stop_type="PICKUP",
                        farmer_id=batch.farmer_id,
                        harvest_batch_id=batch.id,
                        latitude=point[0],
                        longitude=point[1],
                        sequence_number=idx,
                        planned_arrival_time=now + timedelta(minutes=idx * 20),
                        status="PLANNED",
                    )
                )
            else:
                stops.append(
                    RouteStop(
                        route_plan_id=route.id,
                        stop_type="DROP_OFF" if destination_type == "BUYER" else "COLD_HUB",
                        buyer_id=getattr(destination, "id", None) if destination_type == "BUYER" else None,
                        cold_hub_id=getattr(destination, "id", None) if destination_type == "COLD_HUB" else None,
                        latitude=point[0],
                        longitude=point[1],
                        sequence_number=idx,
                        planned_arrival_time=now + timedelta(minutes=idx * 20),
                        status="PLANNED",
                    )
                )

        self.repo.create_stops(stops)

        jobs = []
        for batch in batches:
            jobs.append(
                TransportJob(
                    route_plan_id=route.id,
                    harvest_batch_id=batch.id,
                    buyer_demand_id=None,
                    transporter_id=selected_vehicle.transporter_id,
                    vehicle_id=selected_vehicle.id,
                    agreed_transport_fee=max(500.0, batch.quantity_kg * 2),
                )
            )
        self.repo.create_jobs(jobs)

        self.db.commit()
        return {
            "route_id": str(route.id),
            "route_code": route.route_code,
            "total_distance_km": route.total_distance_km,
            "estimated_duration_minutes": route.estimated_duration_minutes,
            "route_polyline": route.route_polyline,
            "jobs_created": len(jobs),
        }

    def assign_vehicle(self, route_id, vehicle_id):
        route = self.repo.get_route(route_id)
        if not route:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Route not found")
        vehicle = self.db.get(Vehicle, vehicle_id)
        if not vehicle:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found")
        route.vehicle_id = vehicle.id
        route.transporter_id = vehicle.transporter_id
        self.db.commit()
        self.db.refresh(route)
        return route

    def update_route(self, route_id, payload: dict):
        route = self.repo.get_route(route_id)
        if not route:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Route not found")
        for key, value in payload.items():
            if hasattr(route, key):
                setattr(route, key, value)
        self.db.commit()
        self.db.refresh(route)
        return route

    def start_route(self, route_id):
        route = self.repo.get_route(route_id)
        if not route:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Route not found")
        route.status = RouteStatus.ACTIVE
        self.db.commit()
        self.db.refresh(route)
        return route

    def complete_route(self, route_id):
        route = self.repo.get_route(route_id)
        if not route:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Route not found")
        route.status = RouteStatus.COMPLETED
        self.db.commit()
        self.db.refresh(route)
        return route

    def route_stops(self, route_id):
        route = self.repo.get_route(route_id)
        if not route:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Route not found")
        return self.db.scalars(select(RouteStop).where(RouteStop.route_plan_id == route_id).order_by(RouteStop.sequence_number)).all()

    async def route_map(self, route_id):
        route = self.repo.get_route(route_id)
        if not route:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Route not found")
        stops = self.route_stops(route_id)
        points = [(stop.latitude, stop.longitude) for stop in stops]
        if self.provider and points:
            polyline = await self.provider.get_route_polyline(points)
            if polyline:
                route.route_polyline = polyline
                self.db.commit()
                self.db.refresh(route)
        return {"route_id": str(route.id), "route_polyline": route.route_polyline}
