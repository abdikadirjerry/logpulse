"""
Pydantic schemas for alert rule validation and serialization.
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class AlertRuleBase(BaseModel):
    """Base schema with shared alert rule fields."""
    name: str = Field(..., min_length=1, max_length=100)
    log_level: str = Field(default="ERROR")
    threshold_count: int = Field(default=5, ge=1)
    is_active: bool = Field(default=True)


class AlertRuleCreate(AlertRuleBase):
    """Schema for creating a new alert rule."""
    app_id: int


class AlertRuleResponse(AlertRuleBase):
    """Schema for alert rule responses returned by the API."""
    id: int
    app_id: int
    created_at: datetime

    class Config:
        from_attributes = True