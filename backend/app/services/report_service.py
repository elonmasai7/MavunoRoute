from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.buyer import BuyerProfile
from app.models.enums import DeliveryStatus, HarvestBatchStatus, RouteStatus
from app.models.harvest_batch import HarvestBatch
from app.models.payment import Payment
from app.models.route_plan import RoutePlan
from app.models.temperature_event import TemperatureEvent
from app.models.transport_job import TransportJob
from app.models.farmer import FarmerProfile


class ReportService:
    def __init__(self, db: Session):
        self.db = db

    def dashboard_metrics(self) -> dict:
        total_farmers = self.db.query(FarmerProfile).count()
        total_buyers = self.db.query(BuyerProfile).count()
        active_harvest_batches = self.db.query(HarvestBatch).filter(HarvestBatch.status != HarvestBatchStatus.DELIVERED).count()
        active_routes = self.db.query(RoutePlan).filter(RoutePlan.status == RouteStatus.ACTIVE).count()
        completed_deliveries = self.db.query(TransportJob).filter(TransportJob.delivery_status == DeliveryStatus.DELIVERED).count()
        total_transaction_value = float(self.db.query(func.coalesce(func.sum(Payment.amount), 0)).scalar() or 0)
        spoilage_risk_alerts = self.db.query(HarvestBatch).filter(HarvestBatch.spoilage_risk_score >= 61).count()
        cold_chain_breaches = self.db.query(TemperatureEvent).filter(TemperatureEvent.temperature_celsius > 10).count()

        return {
            "total_farmers": total_farmers,
            "total_buyers": total_buyers,
            "active_harvest_batches": active_harvest_batches,
            "active_routes": active_routes,
            "completed_deliveries": completed_deliveries,
            "total_transaction_value": total_transaction_value,
            "spoilage_risk_alerts": spoilage_risk_alerts,
            "cold_chain_breaches": cold_chain_breaches,
        }
