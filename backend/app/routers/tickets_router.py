import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db.db import SessionLocal
from ..schemas.ticket import TicketOut
from ..schemas.ticket_update import TicketUpdate
from ..services.tickets_service import (
    get_all_tickets,
    update_ticket_classification,
    sync_github_labels_for_ticket,
)

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
    return get_all_tickets(db)


@router.post("/classified/{id}")
async def classify_ticket(id: int, data: TicketUpdate, db: Session = Depends(get_db)):
    updated = update_ticket_classification(id, data, db)
    if not updated:
        raise HTTPException(status_code=404, detail="Ticket not found")

    repo = os.getenv("GITHUB_REPO")
    owner = os.getenv("GITHUB_OWNER")

    if not repo or not owner:
        raise HTTPException(status_code=500, detail="GitHub config missing in .env")

    try:
        await sync_github_labels_for_ticket(updated, repo, owner)
    except Exception as e:
        print("Error updating labels in GitHub:", str(e))

    return {"message": "Ticket updated", "id": id}
