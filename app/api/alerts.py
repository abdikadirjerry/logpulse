"""
REST API endpoints for alert rule configuration and evaluation.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.core.database import get_db
from app.models.application import Application
from app.models.alert_rule import AlertRule
from app.models.log_entry import LogEntry
from app.schemas.alert_rule import AlertRuleCreate, AlertRuleResponse

router = APIRouter(prefix="/api/alerts", tags=["Alerts"])


@router.get("/", response_model=List[AlertRuleResponse])
def get_alert_rules(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Retrieve all configured alert rules."""
    rules = db.query(AlertRule).offset(skip).limit(limit).all()
    return rules


@router.post("/", response_model=AlertRuleResponse, status_code=status.HTTP_201_CREATED)
def create_alert_rule(rule_in: AlertRuleCreate, db: Session = Depends(get_db)):
    """Create a new alert rule for an application."""
    app = db.query(Application).filter(Application.id == rule_in.app_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")

    new_rule = AlertRule(
        app_id=rule_in.app_id,
        name=rule_in.name,
        log_level=rule_in.log_level.upper(),
        threshold_count=rule_in.threshold_count,
        is_active=rule_in.is_active,
    )
    db.add(new_rule)
    db.commit()
    db.refresh(new_rule)
    return new_rule


@router.get("/evaluate/{app_id}", response_model=Dict[str, Any])
def evaluate_application_alerts(app_id: int, db: Session = Depends(get_db)):
    """Evaluate active alert rules against current log error counts for an application."""
    app = db.query(Application).filter(Application.id == app_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")

    rules = db.query(AlertRule).filter(AlertRule.app_id == app_id, AlertRule.is_active == True).all()
    
    evaluations = []
    triggered_count = 0

    for rule in rules:
        current_count = (
            db.query(LogEntry)
            .filter(LogEntry.app_id == app_id, LogEntry.level == rule.log_level)
            .count()
        )
        is_triggered = current_count >= rule.threshold_count
        if is_triggered:
            triggered_count += 1

        evaluations.append({
            "rule_id": rule.id,
            "rule_name": rule.name,
            "log_level": rule.log_level,
            "threshold": rule.threshold_count,
            "current_count": current_count,
            "triggered": is_triggered,
        })

    return {
        "app_id": app_id,
        "app_name": app.name,
        "total_rules_evaluated": len(rules),
        "triggered_alerts": triggered_count,
        "evaluations": evaluations,
    }


@router.delete("/{rule_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_alert_rule(rule_id: int, db: Session = Depends(get_db)):
    """Delete an alert rule."""
    rule = db.query(AlertRule).filter(AlertRule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Alert rule not found")

    db.delete(rule)
    db.commit()
    return None