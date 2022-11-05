"""Model Schemas."""

from pydantic import BaseModel
from models import ComplaintStatus, ComplaintPriority
from datetime import datetime
from typing import Optional


class ComplaintBase(BaseModel):
    """Complaint Base Model."""

    complaint: str
    status: Optional[ComplaintStatus]


class ComplaintCreate(ComplaintBase):
    """Complaint Create Model."""

    pass


class ComplaintUpdate(BaseModel):
    """Complaint Status."""

    status: ComplaintStatus


class Complaint(ComplaintBase):
    """Complaint Class."""

    id: int
    user_id: int
    created: datetime
    priority: ComplaintPriority
    last_updated: datetime

    class Config:
        orm_mode = True


class ComplaintUpdatesBase(BaseModel):
    """Complaint Updates Base Model."""

    status_update: ComplaintStatus
    log: str


class ComplaintUpdatesCreate(ComplaintUpdatesBase):
    """Complaint Updates Base Model."""

    pass


class ComplaintUpdates(ComplaintBase):
    """Complaint Class."""

    id: int
    complaint_id: int
    created: datetime

    class Config:
        orm_mode = True
