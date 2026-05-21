from uuid import uuid4

from app.services.buyer_demand_service import BuyerDemandService
from app.services.matching_service import MatchingService


def test_match_harvest_to_demand(client, monkeypatch):
    class DemandObj:
        id = uuid4()

    monkeypatch.setattr(BuyerDemandService, "get", lambda self, demand_id: DemandObj())
    monkeypatch.setattr(
        MatchingService,
        "match_harvest_to_demand",
        lambda self, demand: {
            "buyer_demand_id": str(demand.id),
            "matches": [{"harvest_batch_id": str(uuid4()), "match_score": 91, "reason": "Feasible"}],
        },
    )
    response = client.post("/api/v1/matching/harvest-to-demand", json={"buyer_demand_id": str(uuid4())})
    assert response.status_code == 200
    assert len(response.json()["data"]["matches"]) == 1
