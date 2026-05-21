from fastapi import APIRouter

from app.api.v1.routes import (
    admin,
    auth,
    buyer_demands,
    buyers,
    cold_hubs,
    cooperatives,
    crops,
    farmers,
    harvest_batches,
    health,
    matching,
    mpesa,
    notifications,
    payments,
    proof_events,
    reports,
    route_stops,
    routes,
    temperature_events,
    transporters,
    transport_jobs,
    users,
    vehicles,
    weather,
)

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(cooperatives.router)
api_router.include_router(farmers.router)
api_router.include_router(crops.router)
api_router.include_router(harvest_batches.router)
api_router.include_router(buyers.router)
api_router.include_router(buyer_demands.router)
api_router.include_router(matching.router)
api_router.include_router(transporters.router)
api_router.include_router(vehicles.router)
api_router.include_router(cold_hubs.router)
api_router.include_router(routes.router)
api_router.include_router(route_stops.router)
api_router.include_router(transport_jobs.router)
api_router.include_router(proof_events.router)
api_router.include_router(temperature_events.router)
api_router.include_router(payments.router)
api_router.include_router(mpesa.router)
api_router.include_router(notifications.router)
api_router.include_router(weather.router)
api_router.include_router(reports.router)
api_router.include_router(admin.router)
api_router.include_router(health.router)
