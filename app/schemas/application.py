"""
Pydantic schemas for application validation and serialization.
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class ApplicationBase(BaseModel):
    """Base schema with shared application fields."""
    name: str = Field(..., min_length=1, max_length=100)
    environment: str = Field(default="production")
    description: Optional[str] = None


class ApplicationCreate(ApplicationBase):
    """Schema for registering a new application."""
    pass


class ApplicationResponse(ApplicationBase):
    """Schema for application responses returned by the API."""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True