from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from app.web.dependencies import WebUser, require_web_role
from app.web.utils import templates

router = APIRouter(prefix="/cold-hub", tags=["Web - Cold Hub"])


@router.get("/dashboard", response_class=HTMLResponse)
def coldhub_dashboard(request: Request, web_user: WebUser = Depends(require_web_role("COLD_HUB_OPERATOR"))):
    return templates.TemplateResponse(
        "pages/cold_hub/dashboard.html",
        {"request": request, "user": web_user, "active_page": "coldhub_dashboard"},
    )


@router.get("/capacity", response_class=HTMLResponse)
def coldhub_capacity(request: Request, web_user: WebUser = Depends(require_web_role("COLD_HUB_OPERATOR"))):
    return templates.TemplateResponse(
        "pages/cold_hub/capacity.html",
        {"request": request, "user": web_user, "active_page": "coldhub_capacity"},
    )


@router.get("/check-in", response_class=HTMLResponse)
def coldhub_checkin(request: Request, web_user: WebUser = Depends(require_web_role("COLD_HUB_OPERATOR"))):
    return templates.TemplateResponse(
        "pages/cold_hub/checkin.html",
        {"request": request, "user": web_user, "active_page": "coldhub_checkin"},
    )


@router.get("/check-out", response_class=HTMLResponse)
def coldhub_checkout(request: Request, web_user: WebUser = Depends(require_web_role("COLD_HUB_OPERATOR"))):
    return templates.TemplateResponse(
        "pages/cold_hub/checkout.html",
        {"request": request, "user": web_user, "active_page": "coldhub_checkout"},
    )


@router.get("/temperature-logs", response_class=HTMLResponse)
def coldhub_templogs(request: Request, web_user: WebUser = Depends(require_web_role("COLD_HUB_OPERATOR"))):
    return templates.TemplateResponse(
        "pages/cold_hub/temperature_logs.html",
        {"request": request, "user": web_user, "active_page": "coldhub_templogs"},
    )


@router.get("/breaches", response_class=HTMLResponse)
def coldhub_breaches(request: Request, web_user: WebUser = Depends(require_web_role("COLD_HUB_OPERATOR"))):
    return templates.TemplateResponse(
        "pages/cold_hub/breaches.html",
        {"request": request, "user": web_user, "active_page": "coldhub_breaches"},
    )
