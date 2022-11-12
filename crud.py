"""Complaints CRUD."""

from datetime import datetime
from typing import Optional
from fastapi import HTTPException

from sqlalchemy.orm import Session

import models
import schemas


def get_complaint(db: Session, complaint_id: int):
    """Get Complaint."""
    return db.query(models.Complaint)\
        .filter(models.Complaint.id == complaint_id)\
        .first()


def get_complaints(db: Session, skip: int = 0, limit: int = 100,
                   user_id: Optional[int] = None,
                   start_date: Optional[datetime] = None,
                   end_date: Optional[datetime] = None):
    """Get All Complaints."""
    query = db.query(models.Complaint)
    if user_id is not None:
        query = query.filter(models.Complaint.user_id == user_id)
    if start_date is not None:
        query = query.filter(models.Complaint.created >= start_date)
    if end_date is not None:
        query = query.filter(models.Complaint.created <= end_date)
    query = query.order_by(models.Complaint.priority.desc())
    query = query.offset(skip).limit(limit)
    return query.all()


def create_complaint(db: Session, user_id: int, complaint: schemas.ComplaintCreate):
    """Create Complaint."""
    db_complaint = models.Complaint()
    db_complaint.user_id = user_id
    db_complaint.complaint = complaint.complaint
    db.add(db_complaint)
    db.commit()
    db.refresh(db_complaint)
    return db_complaint


def update_complaint_status(db: Session, complaint_id: int, status: models.ComplaintStatus):
    """Update Comment Status."""
    db_complaint = get_complaint(db, complaint_id)
    if status.value > db_complaint.status.value:
        db_complaint_update = models.ComplaintUpdates()
        db_complaint_update.complaint_id = complaint_id
        db_complaint_update.log = f'Updated status to {status.name}'
        db_complaint_update.status_update = status

        db_complaint.status = status
        db.add(db_complaint)
        db.add(db_complaint_update)
        db.commit()
    db.refresh(db_complaint)
    return db_complaint


def escalate_complaint(db: Session, complaint_id: int, user: dict):
    """Escalate Complaint."""
    db_complaint: schemas.Complaint = get_complaint(db, complaint_id)
    if user['role'] != 'employee' and user['user_id'] != db_complaint.user_id:
        raise HTTPException(401, "Access Denied")
    db_complaint.priority = models.ComplaintPriority.ESCALATED
    db.add(db_complaint)
    db.commit()
    db.refresh(db_complaint)
    return db_complaint
