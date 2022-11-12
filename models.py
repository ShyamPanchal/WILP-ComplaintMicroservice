"""DB Models."""

from sqlalchemy import DateTime, Column, Integer, String, Enum, ForeignKey
import datetime
import enum

from database import Base


class ComplaintStatus(enum.Enum):
    """Complaint Status Enum."""

    ACTIVE = 1
    PROGRESS = 2
    HOLD = 3
    COMPLETE = 4


class ComplaintPriority(enum.Enum):
    """Complaint Priority Enum."""

    IMPORTANT = 0
    VERY_IMPORTANT = 1
    PRIORITY = 3
    ESCALATED = 4


class Complaint(Base):
    """Complaint Model."""

    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=False, index=True)
    complaint = Column(String)
    status = Column(Enum(ComplaintStatus), default=ComplaintStatus.ACTIVE)

    priority = Column(Enum(ComplaintPriority),
                      default=ComplaintPriority.IMPORTANT)

    created = Column(DateTime, default=datetime.datetime.utcnow())
    last_updated = Column(DateTime, default=datetime.datetime.utcnow())


class ComplaintUpdates(Base):
    """Complaint Updates Model."""

    __tablename__ = "complaint_updates"

    id = Column(Integer, primary_key=True, index=True)
    complaint_id = Column(Integer, ForeignKey("complaints.id"))
    created = Column(DateTime, default=datetime.datetime.utcnow())
    status_update = Column(Enum(ComplaintStatus))
    log = Column(String)
