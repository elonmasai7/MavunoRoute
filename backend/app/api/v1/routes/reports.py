from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import require_permission
from app.models.buyer_demand import BuyerDemand
from app.models.enums import DeliveryStatus, RouteStatus
from app.models.harvest_batch import HarvestBatch
from app.models.payment import Payment
from app.models.route_plan import RoutePlan
from app.models.temperature_event import TemperatureEvent
from app.models.transport_job import TransportJob
from app.services.report_service import ReportService
from app.utils.response import success_response

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db), _=Depends(require_permission("reports:read"))):
    data = ReportService(db).dashboard_metrics()
    return success_response("Records retrieved successfully", data)


@router.get("/farmer-income")
def farmer_income(db: Session = Depends(get_db), _=Depends(require_permission("reports:read"))):
    total = float(db.query(Payment.amount).count() and sum(float(x.amount) for x in db.query(Payment).all()) or 0)
    return success_response("Records retrieved successfully", {"total_farmer_income": total, "currency": "KES"})


@router.get("/post-harvest-loss")
def post_harvest_loss(db: Session = Depends(get_db), _=Depends(require_permission("reports:read"))):
    risky = db.query(HarvestBatch).filter(HarvestBatch.spoilage_risk_score >= 61).count()
    total = db.query(HarvestBatch).count() or 1
    return success_response("Records retrieved successfully", {"high_risk_batches": risky, "risk_ratio": round(risky / total, 4)})


@router.get("/route-performance")
def route_performance(db: Session = Depends(get_db), _=Depends(require_permission("reports:read"))):
    routes = db.query(RoutePlan).count()
    completed = db.query(RoutePlan).filter(RoutePlan.status == RouteStatus.COMPLETED).count()
    return success_response("Records retrieved successfully", {"total_routes": routes, "completed_routes": completed})


@router.get("/transporter-performance")
def transporter_performance(db: Session = Depends(get_db), _=Depends(require_permission("reports:read"))):
    completed_jobs = db.query(TransportJob).filter(TransportJob.delivery_status == DeliveryStatus.DELIVERED).count()
    total_jobs = db.query(TransportJob).count()
    return success_response("Records retrieved successfully", {"completed_jobs": completed_jobs, "total_jobs": total_jobs})


@router.get("/buyer-demand")
def buyer_demand(db: Session = Depends(get_db), _=Depends(require_permission("reports:read"))):
    total_demands = db.query(BuyerDemand).count()
    return success_response("Records retrieved successfully", {"total_demands": total_demands})


@router.get("/cold-chain-breaches")
def cold_chain_breaches(db: Session = Depends(get_db), _=Depends(require_permission("reports:read"))):
    breaches = db.query(TemperatureEvent).filter(TemperatureEvent.temperature_celsius > 10).count()
    return success_response("Records retrieved successfully", {"breaches": breaches})


@router.get("/payments")
def payment_report(db: Session = Depends(get_db), _=Depends(require_permission("reports:read"))):
    total = float(sum(float(item.amount) for item in db.query(Payment).all()))
    return success_response("Records retrieved successfully", {"total_payment_value": total, "currency": "KES"})
