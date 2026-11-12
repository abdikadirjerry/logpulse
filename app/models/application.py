"""
SQLAlchemy ORM model for monitored applications.
"""

from sqlalchemy import Column, Integer, String, DateTime, func
from app.core.database import Base


class Application(Base):
    """Application model representing services sending logs to LogPulse."""

    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    environment = Column(String(50), default="production")  # production, staging, development
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())