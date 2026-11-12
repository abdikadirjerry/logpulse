"""
LogPulse Main FastAPI Application Entrypoint.
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse

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

# Include all API routers
app.include_router(applications.router)
app.include_router(logs.router)
app.include_router(analytics.router)
app.include_router(alerts.router)


@app.get("/health", tags=["Health Check"])
async def health_check():
    """Health check endpoint to verify backend service status."""
    return JSONResponse(status_code=200, content={"status": "healthy", "service": "LogPulse API"})