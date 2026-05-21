from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.models.crop import Crop
from app.models.harvest_batch import HarvestBatch


class SpoilageRiskService:
    def __init__(self, db: Session):
        self.db = db

    def calculate(self, batch: HarvestBatch, crop: Crop, weather_temperature_c: float | None, route_duration_minutes: int | None) -> dict:
        now = datetime.now(UTC)
        harvest_time = batch.actual_harvest_datetime or batch.expected_harvest_datetime
        age_hours = max((now - harvest_time).total_seconds() / 3600, 0)
        perishability_component = min(crop.perishability_level * 7, 35)
        age_component = min((age_hours / max(crop.shelf_life_hours, 1)) * 30, 30)

        weather_component = 0
        explanation = []
        if weather_temperature_c is not None:
            if weather_temperature_c > crop.ideal_temperature_max:
                weather_component = min((weather_temperature_c - crop.ideal_temperature_max) * 2, 15)
                explanation.append("Current weather is above ideal handling temperature")

        route_component = min(((route_duration_minutes or 0) / 60) * 2, 10)
        packaging_component = 5 if batch.packaging_type.upper() in {"SACK", "LOOSE"} else 1

        score = int(min(perishability_component + age_component + weather_component + route_component + packaging_component, 100))

        if score <= 30:
            level = "LOW"
            action = "Proceed with normal dispatch"
        elif score <= 60:
            level = "MEDIUM"
            action = "Dispatch within 8 hours"
        elif score <= 80:
            level = "HIGH"
            action = "Dispatch within 3 hours"
        else:
            level = "CRITICAL"
            action = "Immediate cold-chain dispatch required"

        if crop.perishability_level >= 7:
            explanation.append(f"{crop.name} has high perishability")
        if age_hours > 8:
            explanation.append("Harvest batch is older than 8 hours")
        if not explanation:
            explanation.append("Risk factors are within acceptable thresholds")

        estimated_value_at_risk = round(float(batch.quantity_kg * batch.asking_price_per_kg) * (score / 100), 2)

        return {
            "harvest_batch_id": str(batch.id),
            "risk_score": score,
            "risk_level": level,
            "recommended_action": action,
            "estimated_value_at_risk": estimated_value_at_risk,
            "explanation": explanation,
        }
