"""
REST API endpoints for managing monitored applications.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.application import Application
from app.schemas.application import ApplicationCreate, ApplicationResponse

router = APIRouter(prefix="/api/applications", tags=["Applications"])


@router.get("/", response_model=List[ApplicationResponse])
def get_applications(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Retrieve all registered applications."""
    apps = db.query(Application).offset(skip).limit(limit).all()
    return apps


@router.post("/", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
def register_application(app_in: ApplicationCreate, db: Session = Depends(get_db)):
    """Register a new application."""
    existing = db.query(Application).filter(Application.name == app_in.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Application with this name already exists")

    new_app = Application(
        name=app_in.name,
        environment=app_in.environment,
        description=app_in.description,
    )
    db.add(new_app)
    db.commit()
    db.refresh(new_app)
    return new_app


@router.get("/{app_id}", response_model=ApplicationResponse)
def get_application(app_id: int, db: Session = Depends(get_db)):
    """Retrieve a single application by ID."""
    app = db.query(Application).filter(Application.id == app_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    return app