from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from app.web.dependencies import WebUser, require_web_role
from app.web.utils import templates

router = APIRouter(prefix="/buyer", tags=["Web - Buyer"])


@router.get("/dashboard", response_class=HTMLResponse)
def buyer_dashboard(request: Request, web_user: WebUser = Depends(require_web_role("BUYER"))):
    return templates.TemplateResponse(
        "pages/buyer/dashboard.html",
        {"request": request, "user": web_user, "active_page": "buyer_dashboard"},
    )


@router.get("/demands", response_class=HTMLResponse)
def buyer_demands(request: Request, web_user: WebUser = Depends(require_web_role("BUYER"))):
    return templates.TemplateResponse(
        "pages/buyer/demands.html",
        {"request": request, "user": web_user, "active_page": "buyer_demands"},
    )


@router.get("/demands/create", response_class=HTMLResponse)
def buyer_demands_create(request: Request, web_user: WebUser = Depends(require_web_role("BUYER"))):
    return templates.TemplateResponse(
        "pages/buyer/demands_create.html",
        {"request": request, "user": web_user, "active_page": "buyer_demands_create"},
    )


@router.get("/demands/{demand_id}", response_class=HTMLResponse)
def buyer_demand_detail(request: Request, demand_id: str, web_user: WebUser = Depends(require_web_role("BUYER"))):
    return templates.TemplateResponse(
        "pages/buyer/demand_detail.html",
        {"request": request, "user": web_user, "active_page": "buyer_demands", "demand_id": demand_id},
    )


@router.get("/matches", response_class=HTMLResponse)
def buyer_matches(request: Request, web_user: WebUser = Depends(require_web_role("BUYER"))):
    return templates.TemplateResponse(
        "pages/buyer/matches.html",
        {"request": request, "user": web_user, "active_page": "buyer_matches"},
    )


@router.get("/orders", response_class=HTMLResponse)
def buyer_orders(request: Request, web_user: WebUser = Depends(require_web_role("BUYER"))):
    return templates.TemplateResponse(
        "pages/buyer/orders.html",
        {"request": request, "user": web_user, "active_page": "buyer_orders"},
    )


@router.get("/orders/{order_id}", response_class=HTMLResponse)
def buyer_order_detail(request: Request, order_id: str, web_user: WebUser = Depends(require_web_role("BUYER"))):
    return templates.TemplateResponse(
        "pages/buyer/order_detail.html",
        {"request": request, "user": web_user, "active_page": "buyer_orders", "order_id": order_id},
    )


@router.get("/payments", response_class=HTMLResponse)
def buyer_payments(request: Request, web_user: WebUser = Depends(require_web_role("BUYER"))):
    return templates.TemplateResponse(
        "pages/buyer/payments.html",
        {"request": request, "user": web_user, "active_page": "buyer_payments"},
    )


@router.get("/deliveries", response_class=HTMLResponse)
def buyer_deliveries(request: Request, web_user: WebUser = Depends(require_web_role("BUYER"))):
    return templates.TemplateResponse(
        "pages/buyer/deliveries.html",
        {"request": request, "user": web_user, "active_page": "buyer_deliveries"},
    )
