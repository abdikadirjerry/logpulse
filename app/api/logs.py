"""
REST API endpoints for log ingestion and filtering.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.models.application import Application
from app.models.log_entry import LogEntry
from app.schemas.log_entry import LogEntryCreate, LogEntryResponse

router = APIRouter(prefix="/api/logs", tags=["Logs"])


@router.get("/", response_model=List[LogEntryResponse])
def get_logs(
    app_id: Optional[int] = Query(None, description="Filter by application ID"),
    level: Optional[str] = Query(None, description="Filter by log level (INFO, WARNING, ERROR, FATAL)"),
    module: Optional[str] = Query(None, description="Filter by module name"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Retrieve ingested log entries with optional filters and pagination."""
    query = db.query(LogEntry)
    
    if app_id:
        query = query.filter(LogEntry.app_id == app_id)
    if level:
        query = query.filter(LogEntry.level.ilike(level))
    if module:
        query = query.filter(LogEntry.module.ilike(f"%{module}%"))

    logs = query.order_by(LogEntry.timestamp.desc()).offset(skip).limit(limit).all()
    return logs


@router.post("/", response_model=LogEntryResponse, status_code=status.HTTP_201_CREATED)
def ingest_log(log_in: LogEntryCreate, db: Session = Depends(get_db)):
    """Ingest a new server log entry."""
    # Verify application exists
    app = db.query(Application).filter(Application.id == log_in.app_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")

    new_log = LogEntry(
        app_id=log_in.app_id,
        level=log_in.level.upper(),
        message=log_in.message,
        module=log_in.module,
    )
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return new_log