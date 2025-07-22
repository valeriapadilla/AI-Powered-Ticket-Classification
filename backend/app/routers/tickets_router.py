from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db.db import SessionLocal
from ..schemas.ticket import TicketOut
from ..services.tickets_service import get_all_tickets as fetch_tickets

from typing import List

router = APIRouter(prefix="/tickets", tags=["tickets"])
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/get-tickets", response_model=List[TicketOut])
def get_tickets(db: Session = Depends(get_db)):
    return fetch_tickets(db)

from ..schemas.ticket_update import TicketUpdate
from ..services.tickets_service import update_ticket_classification

@router.post("/classified/{id}")
def classify_ticket(id: int, data: TicketUpdate, db: Session = Depends(get_db)):
    updated = update_ticket_classification(id, data, db)
    if not updated:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return {"message": "Ticket updated", "id": id}
