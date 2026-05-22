from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.api.v1.router import api_router
from app.config import get_settings
from app.middleware import DistributedRateLimiterMiddleware, SecurityHeadersMiddleware
from app.utils.response import error_response
from app.web import web_router
from app.web.utils import templates

settings = get_settings()

app = FastAPI(title=settings.app_name, version="1.0.0", docs_url="/docs", redoc_url="/redoc")
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(DistributedRateLimiterMiddleware)

if settings.cors_allowed_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(item) for item in settings.cors_allowed_origins],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    if not request.url.path.startswith(settings.api_prefix):
        return templates.TemplateResponse("pages/public/500.html", {"request": request}, status_code=422)
    return JSONResponse(
        status_code=422,
        content=error_response("Validation failed", "VALIDATION_ERROR", {"details": exc.errors()}),
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    if not request.url.path.startswith(settings.api_prefix):
        if exc.status_code in {401, 303}:
            return RedirectResponse(url="/login", status_code=302)
        if exc.status_code == 403:
            return templates.TemplateResponse("pages/public/403.html", {"request": request}, status_code=403)
        if exc.status_code == 404:
            return templates.TemplateResponse("pages/public/404.html", {"request": request}, status_code=404)
        if exc.status_code >= 500:
            return templates.TemplateResponse("pages/public/500.html", {"request": request}, status_code=500)

    code = "HTTP_ERROR" if exc.status_code >= 500 else "REQUEST_ERROR"
    return JSONResponse(status_code=exc.status_code, content=error_response(str(exc.detail), code, {}))


@app.exception_handler(Exception)
async def unexpected_exception_handler(request: Request, exc: Exception):
    if not request.url.path.startswith(settings.api_prefix):
        return templates.TemplateResponse("pages/public/500.html", {"request": request}, status_code=500)

    if settings.app_env == "production":
        return JSONResponse(
            status_code=500,
            content=error_response("Unexpected internal server error", "INTERNAL_SERVER_ERROR", {}),
        )
    return JSONResponse(status_code=500, content=error_response(str(exc), "INTERNAL_SERVER_ERROR", {}))


app.include_router(api_router, prefix=settings.api_prefix)
app.include_router(web_router)

frontend_static = Path(__file__).resolve().parents[2] / "frontend" / "static"
if frontend_static.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_static)), name="static")
