"""
SQLAlchemy ORM model for log alert rules.
"""

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.core.database import Base


class AlertRule(Base):
    """AlertRule model representing threshold rules for error notifications."""

    __tablename__ = "alert_rules"

    id = Column(Integer, primary_key=True, index=True)
    app_id = Column(Integer, ForeignKey("applications.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    log_level = Column(String(20), default="ERROR")  # Level to trigger on (ERROR, FATAL)
    threshold_count = Column(Integer, default=5)  # Number of occurrences to trigger alert
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship back to Application
    application = relationship("Application", backref="alert_rules")