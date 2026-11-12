"""
SQLAlchemy ORM model for ingested log entries.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.core.database import Base


class LogEntry(Base):
    """LogEntry model representing structured server log records."""

    __tablename__ = "log_entries"

    id = Column(Integer, primary_key=True, index=True)
    app_id = Column(Integer, ForeignKey("applications.id", ondelete="CASCADE"), nullable=False, index=True)
    level = Column(String(20), nullable=False, index=True)  # INFO, WARNING, ERROR, FATAL
    message = Column(Text, nullable=False)
    module = Column(String(100), nullable=True)  # e.g., auth, database, payment
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    # Relationship back to Application
    application = relationship("Application", backref="logs")