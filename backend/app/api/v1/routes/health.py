from fastapi import APIRouter, Depends
from redis import Redis
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.models.integration_log import ApiIntegrationLog
from app.utils.response import success_response

router = APIRouter(prefix="/health", tags=["Health"])
settings = get_settings()


@router.get("")
def health():
    return success_response("Service is healthy", {"status": "ok"})


@router.get("/database")
def health_database(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return success_response("Database is healthy", {"status": "ok"})


@router.get("/redis")
def health_redis():
    client = Redis.from_url(settings.redis_url)
    ping_ok = client.ping()
    return success_response("Redis is healthy", {"status": "ok" if ping_ok else "down"})


@router.get("/integrations")
def health_integrations(db: Session = Depends(get_db)):
    failed = db.query(ApiIntegrationLog).filter(ApiIntegrationLog.status != "SUCCESS").count()
    return success_response("Integration health retrieved", {"failed_integrations": failed})
