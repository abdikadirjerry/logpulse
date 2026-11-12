"""
LogPulse Main FastAPI Application Entrypoint.
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(
    title="LogPulse API",
    description="Application log analyzer & alert dashboard",
    version="1.0.0",
)


@app.get("/health", tags=["Health Check"])
async def health_check():
    """Health check endpoint to verify backend service status."""
    return JSONResponse(status_code=200, content={"status": "healthy", "service": "LogPulse API"})