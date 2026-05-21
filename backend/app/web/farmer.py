from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from app.web.dependencies import WebUser, require_web_role
from app.web.utils import templates

router = APIRouter(prefix="/farmer", tags=["Web - Farmer"])


@router.get("/dashboard", response_class=HTMLResponse)
def farmer_dashboard(request: Request, web_user: WebUser = Depends(require_web_role("FARMER"))):
    return templates.TemplateResponse(
        "pages/farmer/dashboard.html",
        {"request": request, "user": web_user, "active_page": "farmer_dashboard"},
    )


@router.get("/harvests", response_class=HTMLResponse)
def farmer_harvests(request: Request, web_user: WebUser = Depends(require_web_role("FARMER"))):
    return templates.TemplateResponse(
        "pages/farmer/harvests.html",
        {"request": request, "user": web_user, "active_page": "farmer_harvests"},
    )


@router.get("/harvests/create", response_class=HTMLResponse)
def farmer_harvests_create(request: Request, web_user: WebUser = Depends(require_web_role("FARMER"))):
    return templates.TemplateResponse(
        "pages/farmer/harvests_create.html",
        {"request": request, "user": web_user, "active_page": "farmer_harvests_create"},
    )


@router.get("/harvests/{harvest_id}", response_class=HTMLResponse)
def farmer_harvest_detail(request: Request, harvest_id: str, web_user: WebUser = Depends(require_web_role("FARMER"))):
    return templates.TemplateResponse(
        "pages/farmer/harvest_detail.html",
        {"request": request, "user": web_user, "active_page": "farmer_harvests", "harvest_id": harvest_id},
    )


@router.get("/offers", response_class=HTMLResponse)
def farmer_offers(request: Request, web_user: WebUser = Depends(require_web_role("FARMER"))):
    return templates.TemplateResponse(
        "pages/farmer/offers.html",
        {"request": request, "user": web_user, "active_page": "farmer_offers"},
    )


@router.get("/pickups", response_class=HTMLResponse)
def farmer_pickups(request: Request, web_user: WebUser = Depends(require_web_role("FARMER"))):
    return templates.TemplateResponse(
        "pages/farmer/pickups.html",
        {"request": request, "user": web_user, "active_page": "farmer_pickups"},
    )


@router.get("/payments", response_class=HTMLResponse)
def farmer_payments(request: Request, web_user: WebUser = Depends(require_web_role("FARMER"))):
    return templates.TemplateResponse(
        "pages/farmer/payments.html",
        {"request": request, "user": web_user, "active_page": "farmer_payments"},
    )


@router.get("/reports", response_class=HTMLResponse)
def farmer_reports(request: Request, web_user: WebUser = Depends(require_web_role("FARMER"))):
    return templates.TemplateResponse(
        "pages/farmer/reports.html",
        {"request": request, "user": web_user, "active_page": "farmer_reports"},
    )
