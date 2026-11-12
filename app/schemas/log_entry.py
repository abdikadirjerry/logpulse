"""
Pydantic schemas for log entry validation and serialization.
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class LogEntryBase(BaseModel):
    """Base schema with shared log fields."""
    level: str = Field(default="INFO", description="INFO, WARNING, ERROR, FATAL")
    message: str = Field(..., min_length=1)
    module: Optional[str] = Field(None, max_length=100)


class LogEntryCreate(LogEntryBase):
    """Schema for ingesting a new log entry."""
    app_id: int


class LogEntryResponse(LogEntryBase):
    """Schema for log entry responses returned by the API."""
    id: int
    app_id: int
    timestamp: datetime

    class Config:
        from_attributes = True