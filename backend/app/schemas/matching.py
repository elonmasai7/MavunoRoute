from pydantic import BaseModel


class MatchRequest(BaseModel):
    buyer_demand_id: str


class MatchItem(BaseModel):
    harvest_batch_id: str
    match_score: int
    reason: str


class MatchResponse(BaseModel):
    buyer_demand_id: str
    matches: list[MatchItem]
