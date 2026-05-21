from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from app.web.dependencies import WebUser, require_web_role
from app.web.utils import templates

router = APIRouter(prefix="/transporter", tags=["Web - Transporter"])


@router.get("/dashboard", response_class=HTMLResponse)
def transporter_dashboard(request: Request, web_user: WebUser = Depends(require_web_role("TRANSPORTER"))):
    return templates.TemplateResponse(
        "pages/transporter/dashboard.html",
        {"request": request, "user": web_user, "active_page": "transporter_dashboard"},
    )


@router.get("/vehicles", response_class=HTMLResponse)
def transporter_vehicles(request: Request, web_user: WebUser = Depends(require_web_role("TRANSPORTER"))):
    return templates.TemplateResponse(
        "pages/transporter/vehicles.html",
        {"request": request, "user": web_user, "active_page": "transporter_vehicles"},
    )


@router.get("/vehicles/create", response_class=HTMLResponse)
def transporter_vehicles_create(request: Request, web_user: WebUser = Depends(require_web_role("TRANSPORTER"))):
    return templates.TemplateResponse(
        "pages/transporter/vehicles_create.html",
        {"request": request, "user": web_user, "active_page": "transporter_vehicles_create"},
    )


@router.get("/vehicles/{vehicle_id}", response_class=HTMLResponse)
def transporter_vehicle_detail(request: Request, vehicle_id: str, web_user: WebUser = Depends(require_web_role("TRANSPORTER"))):
    return templates.TemplateResponse(
        "pages/transporter/vehicle_detail.html",
        {"request": request, "user": web_user, "active_page": "transporter_vehicles", "vehicle_id": vehicle_id},
    )


@router.get("/jobs", response_class=HTMLResponse)
def transporter_jobs(request: Request, web_user: WebUser = Depends(require_web_role("TRANSPORTER"))):
    return templates.TemplateResponse(
        "pages/transporter/jobs.html",
        {"request": request, "user": web_user, "active_page": "transporter_jobs"},
    )


@router.get("/jobs/{job_id}", response_class=HTMLResponse)
def transporter_job_detail(request: Request, job_id: str, web_user: WebUser = Depends(require_web_role("TRANSPORTER"))):
    return templates.TemplateResponse(
        "pages/transporter/job_detail.html",
        {"request": request, "user": web_user, "active_page": "transporter_jobs", "job_id": job_id},
    )


@router.get("/routes", response_class=HTMLResponse)
def transporter_routes(request: Request, web_user: WebUser = Depends(require_web_role("TRANSPORTER"))):
    return templates.TemplateResponse(
        "pages/transporter/routes.html",
        {"request": request, "user": web_user, "active_page": "transporter_routes"},
    )


@router.get("/routes/{route_id}", response_class=HTMLResponse)
def transporter_route_detail(request: Request, route_id: str, web_user: WebUser = Depends(require_web_role("TRANSPORTER"))):
    return templates.TemplateResponse(
        "pages/transporter/route_detail.html",
        {"request": request, "user": web_user, "active_page": "transporter_routes", "route_id": route_id},
    )


@router.get("/earnings", response_class=HTMLResponse)
def transporter_earnings(request: Request, web_user: WebUser = Depends(require_web_role("TRANSPORTER"))):
    return templates.TemplateResponse(
        "pages/transporter/earnings.html",
        {"request": request, "user": web_user, "active_page": "transporter_earnings"},
    )
