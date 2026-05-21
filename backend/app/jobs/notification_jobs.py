from app.jobs.worker import celery_app


@celery_app.task(name="notifications.send")
def send_notification(notification_id: str):
    return {"notification_id": notification_id, "status": "QUEUED"}
