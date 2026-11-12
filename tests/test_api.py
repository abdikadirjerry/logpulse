"""
Automated integration tests for LogPulse FastAPI backend endpoints.
"""

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import Base, get_db

# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def setup_function():
    Base.metadata.create_all(bind=engine)


def teardown_function():
    Base.metadata.drop_all(bind=engine)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_register_application_and_ingest_log():
    # Register application
    app_res = client.post(
        "/api/applications/",
        json={"name": "payment-gateway", "environment": "production"},
    )
    assert app_res.status_code == 201
    app_data = app_res.json()
    app_id = app_data["id"]
    assert app_data["name"] == "payment-gateway"

    # Ingest log
    log_res = client.post(
        "/api/logs/",
        json={
            "app_id": app_id,
            "level": "ERROR",
            "message": "Stripe timeout exception",
            "module": "checkout",
        },
    )
    assert log_res.status_code == 201
    log_data = log_res.json()
    assert log_data["level"] == "ERROR"
    assert log_data["module"] == "checkout"

    # Check analytics summary
    analytics_res = client.get("/api/analytics/summary")
    assert analytics_res.status_code == 200
    analytics_data = analytics_res.json()
    assert analytics_data["total_logs"] == 1
    assert analytics_data["total_errors"] == 1