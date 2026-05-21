from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from app.web.dependencies import WebUser, get_web_user
from app.web.utils import templates

router = APIRouter(tags=["Web - Public"])


@router.get("/", response_class=HTMLResponse)
def landing(request: Request, _web_user: WebUser = Depends(get_web_user)):
    return templates.TemplateResponse("landing.html", {"request": request})


@router.get("/about", response_class=HTMLResponse)
def about(request: Request, _web_user: WebUser = Depends(get_web_user)):
    return templates.TemplateResponse("pages/public/about.html", {"request": request})


@router.get("/contact", response_class=HTMLResponse)
def contact(request: Request, _web_user: WebUser = Depends(get_web_user)):
    return templates.TemplateResponse("pages/public/contact.html", {"request": request})


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request, web_user: WebUser = Depends(get_web_user)):
    if web_user.is_authenticated:
        return templates.TemplateResponse("login.html", {"request": request})
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request, _web_user: WebUser = Depends(get_web_user)):
    return templates.TemplateResponse("register.html", {"request": request})


@router.get("/forgot-password", response_class=HTMLResponse)
def forgot_password_page(request: Request, _web_user: WebUser = Depends(get_web_user)):
    return templates.TemplateResponse("pages/public/forgot_password.html", {"request": request})


@router.get("/reset-password", response_class=HTMLResponse)
def reset_password_page(request: Request, _web_user: WebUser = Depends(get_web_user)):
    return templates.TemplateResponse("pages/public/reset_password.html", {"request": request})


@router.get("/403", response_class=HTMLResponse)
def forbidden_page(request: Request, _web_user: WebUser = Depends(get_web_user)):
    return templates.TemplateResponse("pages/public/403.html", {"request": request}, status_code=403)


@router.get("/404", response_class=HTMLResponse)
def not_found_page(request: Request, _web_user: WebUser = Depends(get_web_user)):
    return templates.TemplateResponse("pages/public/404.html", {"request": request}, status_code=404)


@router.get("/500", response_class=HTMLResponse)
def server_error_page(request: Request, _web_user: WebUser = Depends(get_web_user)):
    return templates.TemplateResponse("pages/public/500.html", {"request": request}, status_code=500)
