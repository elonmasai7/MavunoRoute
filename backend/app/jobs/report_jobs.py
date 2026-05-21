from app.jobs.worker import celery_app


@celery_app.task(name="reports.generate")
def generate_report(report_type: str):
    return {"report_type": report_type, "status": "QUEUED"}
