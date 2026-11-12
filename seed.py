"""
Database seed script to populate LogPulse with initial demo services and sample logs.
"""

from app.core.database import SessionLocal, engine, Base
from app.models.application import Application
from app.models.log_entry import LogEntry
from app.models.alert_rule import AlertRule


def seed_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    if db.query(Application).count() > 0:
        print("Database already contains applications. Skipping seed.")
        db.close()
        return

    print("Seeding LogPulse database...")

    # Applications
    auth_service = Application(name="auth-service", environment="production", description="User authentication and OAuth service")
    payment_service = Application(name="payment-service", environment="production", description="Stripe and billing integration service")
    inventory_service = Application(name="inventory-service", environment="staging", description="Product stock and warehouse tracking")

    db.add_all([auth_service, payment_service, inventory_service])
    db.commit()

    # Refresh to get IDs
    db.refresh(auth_service)
    db.refresh(payment_service)

    # Sample Logs
    db.add(LogEntry(app_id=auth_service.id, level="INFO", message="User logged in successfully (ID: 4892)", module="auth"))
    db.add(LogEntry(app_id=auth_service.id, level="WARNING", message="Failed login attempt from IP 192.168.1.50", module="security"))
    db.add(LogEntry(app_id=auth_service.id, level="ERROR", message="Database connection pool exhausted", module="database"))

    db.add(LogEntry(app_id=payment_service.id, level="INFO", message="Webhook received: charge.succeeded", module="webhook"))
    db.add(LogEntry(app_id=payment_service.id, level="FATAL", message="Stripe API gateway timeout (504 Gateway Timeout)", module="stripe"))

    # Alert Rules
    db.add(AlertRule(app_id=payment_service.id, name="Critical Payment Failures", log_level="FATAL", threshold_count=1, is_active=True))
    db.add(AlertRule(app_id=auth_service.id, name="Auth Error Threshold", log_level="ERROR", threshold_count=3, is_active=True))

    db.commit()
    db.close()
    print("LogPulse database seeded successfully!")


if __name__ == "__main__":
    seed_database()