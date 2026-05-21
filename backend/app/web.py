from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

ROOT_DIR = Path(__file__).resolve().parents[2]
templates = Jinja2Templates(directory=str(ROOT_DIR / "frontend" / "templates"))

web_router = APIRouter(tags=["Web"])


@web_router.get("/", response_class=HTMLResponse)
def landing(request: Request):
    return templates.TemplateResponse("landing.html", {"request": request})


@web_router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@web_router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@web_router.get("/app/dashboard", response_class=HTMLResponse)
def dashboard_page(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


@web_router.get("/app/mvp-flow", response_class=HTMLResponse)
def mvp_flow_page(request: Request):
    return templates.TemplateResponse("mvp_flow.html", {"request": request})
