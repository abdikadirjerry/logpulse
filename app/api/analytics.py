"""
REST API endpoints for log analytics and error statistics.
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Dict, Any, Optional

from app.core.database import get_db
from app.models.log_entry import LogEntry
from app.models.application import Application

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])


@router.get("/summary", response_model=Dict[str, Any])
def get_log_analytics(
    app_id: Optional[int] = Query(None, description="Filter analytics by application ID"),
    db: Session = Depends(get_db)
):
    """Calculate aggregate log level counts and system health metrics."""
    query = db.query(LogEntry)
    if app_id:
        query = query.filter(LogEntry.app_id == app_id)

    total_logs = query.count()

    # Count by level
    level_counts_raw = (
        db.query(LogEntry.level, func.count(LogEntry.id))
        .group_by(LogEntry.level)
    )
    if app_id:
        level_counts_raw = level_counts_raw.filter(LogEntry.app_id == app_id)
    
    level_breakdown = {level.upper(): count for level, count in level_counts_raw.all()}

    error_count = level_breakdown.get("ERROR", 0)
    fatal_count = level_breakdown.get("FATAL", 0)
    total_errors = error_count + fatal_count

    error_rate_percentage = (total_errors / total_logs * 100) if total_logs > 0 else 0.0

    return {
        "total_logs": total_logs,
        "total_errors": total_errors,
        "error_rate_percentage": round(error_rate_percentage, 2),
        "level_breakdown": {
            "INFO": level_breakdown.get("INFO", 0),
            "WARNING": level_breakdown.get("WARNING", 0),
            "ERROR": error_count,
            "FATAL": fatal_count,
        }
    }