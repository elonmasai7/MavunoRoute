from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from app.web.dependencies import WebUser, require_web_role
from app.web.utils import templates

router = APIRouter(prefix="/cooperative", tags=["Web - Cooperative"])


@router.get("/dashboard", response_class=HTMLResponse)
def cooperative_dashboard(request: Request, web_user: WebUser = Depends(require_web_role("COOPERATIVE_ADMIN"))):
    return templates.TemplateResponse(
        "pages/cooperative/dashboard.html",
        {"request": request, "user": web_user, "active_page": "cooperative_dashboard"},
    )


@router.get("/farmers", response_class=HTMLResponse)
def cooperative_farmers(request: Request, web_user: WebUser = Depends(require_web_role("COOPERATIVE_ADMIN"))):
    return templates.TemplateResponse(
        "pages/cooperative/farmers.html",
        {"request": request, "user": web_user, "active_page": "cooperative_farmers"},
    )


@router.get("/farmers/create", response_class=HTMLResponse)
def cooperative_farmers_create(request: Request, web_user: WebUser = Depends(require_web_role("COOPERATIVE_ADMIN"))):
    return templates.TemplateResponse(
        "pages/cooperative/farmers_create.html",
        {"request": request, "user": web_user, "active_page": "cooperative_farmers_create"},
    )


@router.get("/farmers/{farmer_id}", response_class=HTMLResponse)
def cooperative_farmer_detail(request: Request, farmer_id: str, web_user: WebUser = Depends(require_web_role("COOPERATIVE_ADMIN"))):
    return templates.TemplateResponse(
        "pages/cooperative/farmer_detail.html",
        {"request": request, "user": web_user, "active_page": "cooperative_farmers", "farmer_id": farmer_id},
    )


@router.get("/harvests", response_class=HTMLResponse)
def cooperative_harvests(request: Request, web_user: WebUser = Depends(require_web_role("COOPERATIVE_ADMIN"))):
    return templates.TemplateResponse(
        "pages/cooperative/harvests.html",
        {"request": request, "user": web_user, "active_page": "cooperative_harvests"},
    )


@router.get("/aggregate-harvests", response_class=HTMLResponse)
def cooperative_aggregate(request: Request, web_user: WebUser = Depends(require_web_role("COOPERATIVE_ADMIN"))):
    return templates.TemplateResponse(
        "pages/cooperative/aggregate_harvests.html",
        {"request": request, "user": web_user, "active_page": "cooperative_aggregate"},
    )


@router.get("/reports", response_class=HTMLResponse)
def cooperative_reports(request: Request, web_user: WebUser = Depends(require_web_role("COOPERATIVE_ADMIN"))):
    return templates.TemplateResponse(
        "pages/cooperative/reports.html",
        {"request": request, "user": web_user, "active_page": "cooperative_reports"},
    )
