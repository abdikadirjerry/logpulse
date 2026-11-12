"""
LogPulse Main FastAPI Application Entrypoint.
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.core.database import engine, Base
from app.api import applications, logs, analytics, alerts
from app.models import Application, LogEntry, AlertRule  # Register models

# Automatically create SQLite tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="LogPulse API",
    description="Application log analyzer & alert dashboard",
    version="1.0.0",
)

# Mount static directory for CSS/JS
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Setup Jinja2 templates directory
templates = Jinja2Templates(directory="app/templates")

# Include all API routers
app.include_router(applications.router)
app.include_router(logs.router)
app.include_router(analytics.router)
app.include_router(alerts.router)


@app.get("/", response_class=HTMLResponse, tags=["Frontend"])
async def read_root(request: Request):
    """Render the main LogPulse frontend dashboard."""
    return templates.TemplateResponse(request=request, name="index.html", context={})


@app.get("/health", tags=["Health Check"])
async def health_check():
    """Health check endpoint to verify backend service status."""
    return JSONResponse(status_code=200, content={"status": "healthy", "service": "LogPulse API"})