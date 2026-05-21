from app.services.report_service import ReportService


def test_dashboard_reports_endpoint(client, monkeypatch):
    monkeypatch.setattr(
        ReportService,
        "dashboard_metrics",
        lambda self: {
            "total_farmers": 10,
            "total_buyers": 3,
            "active_harvest_batches": 4,
            "active_routes": 2,
            "completed_deliveries": 8,
            "total_transaction_value": 10000,
            "spoilage_risk_alerts": 1,
            "cold_chain_breaches": 0,
        },
    )
    response = client.get("/api/v1/reports/dashboard")
    assert response.status_code == 200
    assert response.json()["data"]["total_farmers"] == 10
