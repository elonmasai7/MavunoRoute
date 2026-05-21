from datetime import UTC, datetime, timedelta
from types import SimpleNamespace

from app.services.spoilage_risk_service import SpoilageRiskService


def test_spoilage_risk_deterministic():
    service = SpoilageRiskService(db=None)

    crop = SimpleNamespace(
        name="Tomato",
        perishability_level=8,
        ideal_temperature_min=4,
        ideal_temperature_max=8,
        shelf_life_hours=36,
    )
    batch = SimpleNamespace(
        id="batch-1",
        actual_harvest_datetime=datetime.now(UTC) - timedelta(hours=10),
        expected_harvest_datetime=datetime.now(UTC) - timedelta(hours=10),
        packaging_type="SACK",
        quantity_kg=100,
        asking_price_per_kg=60,
    )

    result = service.calculate(batch, crop, weather_temperature_c=30, route_duration_minutes=120)

    assert result["risk_score"] > 0
    assert result["risk_level"] in {"LOW", "MEDIUM", "HIGH", "CRITICAL"}
    assert len(result["explanation"]) >= 1
