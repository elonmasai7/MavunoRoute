from fastapi import APIRouter

from app.web.admin import router as admin_router
from app.web.buyer import router as buyer_router
from app.web.cold_hub import router as cold_hub_router
from app.web.cooperative import router as cooperative_router
from app.web.farmer import router as farmer_router
from app.web.public import router as public_router
from app.web.shared import router as shared_router
from app.web.transporter import router as transporter_router

web_router = APIRouter()

web_router.include_router(public_router)
web_router.include_router(shared_router)
web_router.include_router(farmer_router)
web_router.include_router(buyer_router)
web_router.include_router(transporter_router)
web_router.include_router(cold_hub_router)
web_router.include_router(cooperative_router)
web_router.include_router(admin_router)
