from app.jobs.worker import celery_app


@celery_app.task(name="routes.recalculate")
def recalculate_route(route_id: str):
    return {"route_id": route_id, "status": "QUEUED"}
