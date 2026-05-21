from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from app.web.dependencies import WebUser, require_web_role
from app.web.utils import templates

router = APIRouter(prefix="/admin", tags=["Web - Admin"])


@router.get("/dashboard", response_class=HTMLResponse)
def admin_dashboard(request: Request, web_user: WebUser = Depends(require_web_role("SUPER_ADMIN", "OPS_ADMIN"))):
    return templates.TemplateResponse(
        "pages/admin/dashboard.html",
        {"request": request, "user": web_user, "active_page": "admin_dashboard"},
    )


@router.get("/users", response_class=HTMLResponse)
def admin_users(request: Request, web_user: WebUser = Depends(require_web_role("SUPER_ADMIN", "OPS_ADMIN"))):
    return templates.TemplateResponse(
        "pages/admin/users.html",
        {"request": request, "user": web_user, "active_page": "admin_users"},
    )


@router.get("/users/{user_id}", response_class=HTMLResponse)
def admin_user_detail(request: Request, user_id: str, web_user: WebUser = Depends(require_web_role("SUPER_ADMIN", "OPS_ADMIN"))):
    return templates.TemplateResponse(
        "pages/admin/user_detail.html",
        {"request": request, "user": web_user, "active_page": "admin_users", "user_id": user_id},
    )


@router.get("/farmers", response_class=HTMLResponse)
def admin_farmers(request: Request, web_user: WebUser = Depends(require_web_role("SUPER_ADMIN", "OPS_ADMIN"))):
    return templates.TemplateResponse(
        "pages/admin/farmers.html",
        {"request": request, "user": web_user, "active_page": "admin_farmers"},
    )


@router.get("/farmers/{farmer_id}", response_class=HTMLResponse)
def admin_farmer_detail(request: Request, farmer_id: str, web_user: WebUser = Depends(require_web_role("SUPER_ADMIN", "OPS_ADMIN"))):
    return templates.TemplateResponse(
        "pages/admin/farmer_detail.html",
        {"request": request, "user": web_user, "active_page": "admin_farmers", "farmer_id": farmer_id},
    )


@router.get("/buyers", response_class=HTMLResponse)
def admin_buyers(request: Request, web_user: WebUser = Depends(require_web_role("SUPER_ADMIN", "OPS_ADMIN"))):
    return templates.TemplateResponse(
        "pages/admin/buyers.html",
        {"request": request, "user": web_user, "active_page": "admin_buyers"},
    )


@router.get("/buyers/{buyer_id}", response_class=HTMLResponse)
def admin_buyer_detail(request: Request, buyer_id: str, web_user: WebUser = Depends(require_web_role("SUPER_ADMIN", "OPS_ADMIN"))):
    return templates.TemplateResponse(
        "pages/admin/buyer_detail.html",
        {"request": request, "user": web_user, "active_page": "admin_buyers", "buyer_id": buyer_id},
    )


@router.get("/transporters", response_class=HTMLResponse)
def admin_transporters(request: Request, web_user: WebUser = Depends(require_web_role("SUPER_ADMIN", "OPS_ADMIN"))):
    return templates.TemplateResponse(
        "pages/admin/transporters.html",
        {"request": request, "user": web_user, "active_page": "admin_transporters"},
    )


@router.get("/transporters/{transporter_id}", response_class=HTMLResponse)
def admin_transporter_detail(request: Request, transporter_id: str, web_user: WebUser = Depends(require_web_role("SUPER_ADMIN", "OPS_ADMIN"))):
    return templates.TemplateResponse(
        "pages/admin/transporter_detail.html",
        {"request": request, "user": web_user, "active_page": "admin_transporters", "transporter_id": transporter_id},
    )


@router.get("/vehicles", response_class=HTMLResponse)
def admin_vehicles(request: Request, web_user: WebUser = Depends(require_web_role("SUPER_ADMIN", "OPS_ADMIN"))):
    return templates.TemplateResponse(
        "pages/admin/vehicles.html",
        {"request": request, "user": web_user, "active_page": "admin_vehicles"},
    )


@router.get("/vehicles/{vehicle_id}", response_class=HTMLResponse)
def admin_vehicle_detail(request: Request, vehicle_id: str, web_user: WebUser = Depends(require_web_role("SUPER_ADMIN", "OPS_ADMIN"))):
    return templates.TemplateResponse(
        "pages/admin/vehicle_detail.html",
        {"request": request, "user": web_user, "active_page": "admin_vehicles", "vehicle_id": vehicle_id},
    )


@router.get("/harvests", response_class=HTMLResponse)
def admin_harvests(request: Request, web_user: WebUser = Depends(require_web_role("SUPER_ADMIN", "OPS_ADMIN"))):
    return templates.TemplateResponse(
        "pages/admin/harvests.html",
        {"request": request, "user": web_user, "active_page": "admin_harvests"},
    )


@router.get("/harvests/{harvest_id}", response_class=HTMLResponse)
def admin_harvest_detail(request: Request, harvest_id: str, web_user: WebUser = Depends(require_web_role("SUPER_ADMIN", "OPS_ADMIN"))):
    return templates.TemplateResponse(
        "pages/admin/harvest_detail.html",
        {"request": request, "user": web_user, "active_page": "admin_harvests", "harvest_id": harvest_id},
    )


@router.get("/demands", response_class=HTMLResponse)
def admin_demands(request: Request, web_user: WebUser = Depends(require_web_role("SUPER_ADMIN", "OPS_ADMIN"))):
    return templates.TemplateResponse(
        "pages/admin/demands.html",
        {"request": request, "user": web_user, "active_page": "admin_demands"},
    )


@router.get("/demands/{demand_id}", response_class=HTMLResponse)
def admin_demand_detail(request: Request, demand_id: str, web_user: WebUser = Depends(require_web_role("SUPER_ADMIN", "OPS_ADMIN"))):
    return templates.TemplateResponse(
        "pages/admin/demand_detail.html",
        {"request": request, "user": web_user, "active_page": "admin_demands", "demand_id": demand_id},
    )


@router.get("/routes", response_class=HTMLResponse)
def admin_routes(request: Request, web_user: WebUser = Depends(require_web_role("SUPER_ADMIN", "OPS_ADMIN"))):
    return templates.TemplateResponse(
        "pages/admin/routes.html",
        {"request": request, "user": web_user, "active_page": "admin_routes"},
    )


@router.get("/routes/{route_id}", response_class=HTMLResponse)
def admin_route_detail(request: Request, route_id: str, web_user: WebUser = Depends(require_web_role("SUPER_ADMIN", "OPS_ADMIN"))):
    return templates.TemplateResponse(
        "pages/admin/route_detail.html",
        {"request": request, "user": web_user, "active_page": "admin_routes", "route_id": route_id},
    )


@router.get("/transport-jobs", response_class=HTMLResponse)
def admin_jobs(request: Request, web_user: WebUser = Depends(require_web_role("SUPER_ADMIN", "OPS_ADMIN"))):
    return templates.TemplateResponse(
        "pages/admin/transport_jobs.html",
        {"request": request, "user": web_user, "active_page": "admin_jobs"},
    )


@router.get("/transport-jobs/{job_id}", response_class=HTMLResponse)
def admin_job_detail(request: Request, job_id: str, web_user: WebUser = Depends(require_web_role("SUPER_ADMIN", "OPS_ADMIN"))):
    return templates.TemplateResponse(
        "pages/admin/job_detail.html",
        {"request": request, "user": web_user, "active_page": "admin_jobs", "job_id": job_id},
    )


@router.get("/cold-hubs", response_class=HTMLResponse)
def admin_coldhubs(request: Request, web_user: WebUser = Depends(require_web_role("SUPER_ADMIN", "OPS_ADMIN"))):
    return templates.TemplateResponse(
        "pages/admin/cold_hubs.html",
        {"request": request, "user": web_user, "active_page": "admin_coldhubs"},
    )


@router.get("/cold-hubs/{hub_id}", response_class=HTMLResponse)
def admin_coldhub_detail(request: Request, hub_id: str, web_user: WebUser = Depends(require_web_role("SUPER_ADMIN", "OPS_ADMIN"))):
    return templates.TemplateResponse(
        "pages/admin/coldhub_detail.html",
        {"request": request, "user": web_user, "active_page": "admin_coldhubs", "hub_id": hub_id},
    )


@router.get("/payments", response_class=HTMLResponse)
def admin_payments(request: Request, web_user: WebUser = Depends(require_web_role("SUPER_ADMIN", "OPS_ADMIN"))):
    return templates.TemplateResponse(
        "pages/admin/payments.html",
        {"request": request, "user": web_user, "active_page": "admin_payments"},
    )


@router.get("/payments/{payment_id}", response_class=HTMLResponse)
def admin_payment_detail(request: Request, payment_id: str, web_user: WebUser = Depends(require_web_role("SUPER_ADMIN", "OPS_ADMIN"))):
    return templates.TemplateResponse(
        "pages/admin/payment_detail.html",
        {"request": request, "user": web_user, "active_page": "admin_payments", "payment_id": payment_id},
    )


@router.get("/reports", response_class=HTMLResponse)
def admin_reports(request: Request, web_user: WebUser = Depends(require_web_role("SUPER_ADMIN", "OPS_ADMIN"))):
    return templates.TemplateResponse(
        "pages/admin/reports.html",
        {"request": request, "user": web_user, "active_page": "admin_reports"},
    )


@router.get("/audit-logs", response_class=HTMLResponse)
def admin_auditlogs(request: Request, web_user: WebUser = Depends(require_web_role("SUPER_ADMIN", "OPS_ADMIN"))):
    return templates.TemplateResponse(
        "pages/admin/audit_logs.html",
        {"request": request, "user": web_user, "active_page": "admin_auditlogs"},
    )


@router.get("/integration-logs", response_class=HTMLResponse)
def admin_integrationlogs(request: Request, web_user: WebUser = Depends(require_web_role("SUPER_ADMIN", "OPS_ADMIN"))):
    return templates.TemplateResponse(
        "pages/admin/integration_logs.html",
        {"request": request, "user": web_user, "active_page": "admin_integrationlogs"},
    )


@router.get("/system-health", response_class=HTMLResponse)
def admin_health(request: Request, web_user: WebUser = Depends(require_web_role("SUPER_ADMIN", "OPS_ADMIN"))):
    return templates.TemplateResponse(
        "pages/admin/system_health.html",
        {"request": request, "user": web_user, "active_page": "admin_health"},
    )


@router.get("/settings", response_class=HTMLResponse)
def admin_settings(request: Request, web_user: WebUser = Depends(require_web_role("SUPER_ADMIN", "OPS_ADMIN"))):
    return templates.TemplateResponse(
        "pages/admin/settings.html",
        {"request": request, "user": web_user, "active_page": "admin_settings"},
    )
