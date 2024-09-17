from http.client import HTTPException

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.models.models import Event, User, Tickets, TicketPurchase
from app.dependencies import get_db, get_current_user
from app.schemas.request import TicketCreateRequest, TicketPurchaseRequest
from app.schemas.response import TicketResponse, TicketPurchasedResponse

ticketing_router = APIRouter(
    prefix="/events",
    tags=['Ticketing']
)

@ticketing_router.post("/{event_id}/tickets", response_model=TicketResponse)
def create_ticket_for_event(event_id:str, request:TicketCreateRequest, current_user:User = Depends(get_current_user), session: Session = Depends(get_db)):
    """create tickets for an event by the organizers"""
    event = session.query(Event).filter(Event.uid == event_id).first()

    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event does not exist")

    # create a ticket
    ticket = Tickets(
        expiration_date=request.expiration_date,
        price=request.price,
        event = event.id
    )
    session.add(ticket)
    session.commit()
    session.refresh(ticket)

    return ticket

@ticketing_router.post("/{event_id}/register", response_model=TicketPurchasedResponse)
def register_for_event(event_id: str, request:TicketPurchaseRequest, session: Session = Depends(get_db)):
    event = session.query(Event).filter(Event.uid == event_id).first()

    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event does not exist")

    #
    ticket = TicketPurchase(**request)
    session.add(ticket)
    session.commit()
    session.refresh(ticket)
    return ticket
