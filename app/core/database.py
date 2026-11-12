"""
SQLAlchemy database engine and session configuration for LogPulse.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# SQLite database URL for local development
SQLALCHEMY_DATABASE_URL = "sqlite:///./logpulse.db"

# Create SQLAlchemy engine with check_same_thread=False for SQLite concurrency in FastAPI
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# SessionLocal class for individual database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our ORM models
Base = declarative_base()


def get_db():
    """Dependency generator that yields a database session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()