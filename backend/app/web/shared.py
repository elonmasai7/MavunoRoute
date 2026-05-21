from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from app.web.dependencies import WebUser, get_web_user, require_web_auth
from app.web.utils import templates

router = APIRouter(tags=["Web - Shared"])

ROLE_DASHBOARDS = {
    "FARMER": "/farmer/dashboard",
    "BUYER": "/buyer/dashboard",
    "TRANSPORTER": "/transporter/dashboard",
    "COLD_HUB_OPERATOR": "/cold-hub/dashboard",
    "COOPERATIVE_ADMIN": "/cooperative/dashboard",
    "SUPER_ADMIN": "/admin/dashboard",
    "OPS_ADMIN": "/admin/dashboard",
    "FINANCE_PARTNER": "/admin/dashboard",
}


@router.get("/dashboard")
def dashboard_redirect(request: Request):
    web_user = get_web_user(request)
    if not web_user.is_authenticated:
        return RedirectResponse(url="/login", status_code=302)
    target = ROLE_DASHBOARDS.get(web_user.role, "/login")
    return RedirectResponse(url=target, status_code=302)


@router.get("/logout", response_class=HTMLResponse)
def logout(request: Request):
    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie("mavuno_access_token", path="/")
    response.delete_cookie("mavuno_refresh_token", path="/")
    return response


@router.get("/profile", response_class=HTMLResponse)
def profile_page(request: Request, web_user: WebUser = Depends(require_web_auth)):
    return templates.TemplateResponse("pages/shared/profile.html", {"request": request, "user": web_user})


@router.get("/settings", response_class=HTMLResponse)
def settings_page(request: Request, web_user: WebUser = Depends(require_web_auth)):
    return templates.TemplateResponse("pages/shared/settings.html", {"request": request, "user": web_user})
