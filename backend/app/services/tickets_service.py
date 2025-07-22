from sqlalchemy.orm import Session
from ..models.Issue_db import Issue_db, StatusEnum
from ..schemas.ticket_update import TicketUpdate

def get_all_tickets(db: Session):
    tickets = db.query(Issue_db).all()
    print("Tickets desde la base de datos:", tickets)
    return tickets

def update_ticket_classification(ticket_id: int, update_data: TicketUpdate, db: Session):
    ticket = db.query(Issue_db).filter(Issue_db.github_issue_id == ticket_id).first()
    if not ticket:
        return None
    if update_data.level is not None:
        ticket.level_label = update_data.level
    if update_data.priority is not None:
        ticket.priority_label = update_data.priority
    if update_data.eta is not None:
        ticket.eta = update_data.eta
    ticket.status = StatusEnum.IN_PROGRESS.value

    db.commit()
    db.refresh(ticket)
    return ticket
