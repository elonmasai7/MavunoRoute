from pydantic import BaseModel


class DashboardMetrics(BaseModel):
    total_farmers: int
    total_buyers: int
    active_harvest_batches: int
    active_routes: int
    completed_deliveries: int
    total_transaction_value: float
    spoilage_risk_alerts: int
    cold_chain_breaches: int
