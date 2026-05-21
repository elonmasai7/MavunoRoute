from app.jobs.worker import celery_app


@celery_app.task(name="risk.calculate")
def calculate_risk(batch_id: str):
    return {"batch_id": batch_id, "status": "QUEUED"}
