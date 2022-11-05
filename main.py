"""Main API File."""

from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
from typing import Optional
from database import SessionLocal, engine
from datetime import datetime

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    """Get DB."""
    # Dependency
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user(token: str):
    """Get User."""
    if token == '0':
        return {'user_id': 0, 'role': 'complainer'}
    if token == '1':
        return {'user_id': 1, 'role': 'complainer'}
    if token == '2':
        return {'user_id': 2, 'role': 'employee'}
    if token == '3':
        return {'user_id': 3, 'role': 'employee'}
    return None


@app.get("/")
async def root():
    """Root API Endpoint."""
    return {"message": "Application Running"}


@app.post("/complaints/", response_model=schemas.Complaint)
def create_complaint(complaint: schemas.ComplaintCreate,
                     user: Optional[dict] = Depends(get_user),
                     db: Session = Depends(get_db)):
    """Create Complaint."""
    if user is None or user['role'] != 'complainer':
        raise HTTPException(401, "User is not a complainer")
    return crud.create_complaint(db=db, user_id=user['user_id'], complaint=complaint)


@app.get("/complaints/", response_model=List[schemas.Complaint])
def read_complaints(skip: int = 0, limit: int = 100,
                    user_id: Optional[int] = None,
                    start_date: Optional[datetime] = None,
                    end_date: Optional[datetime] = None,
                    db: Session = Depends(get_db)):
    """Get all complaints."""
    return crud.get_complaints(db, skip=skip, limit=limit,
                               user_id=user_id, start_date=start_date,
                               end_date=end_date)


@app.put("/complaints/{complaint_id}", response_model=schemas.Complaint)
def update_complaint_status(complaint_id: int,
                            complaint: schemas.ComplaintUpdate,
                            user: Optional[dict] = Depends(get_user),
                            db: Session = Depends(get_db)):
    """Update Complaint Status."""
    if user is None or user['role'] != 'employee':
        raise HTTPException(401, "User is not a employee")
    return crud.update_complaint_status(db, complaint_id=complaint_id,
                                        status=complaint.status)


@app.put("/complaints/{complaint_id}/escalate",
         response_model=schemas.Complaint)
def escalate_complaint(complaint_id: int,
                       user: Optional[dict] = Depends(get_user),
                       db: Session = Depends(get_db)):
    """Escalate Complaint."""
    if user is None:
        raise HTTPException(401, "User is not a registered")
    return crud.escalate_complaint(db, complaint_id=complaint_id, user=user)
