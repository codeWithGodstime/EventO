from fastapi import APIRouter, Depends, status, HTTPException
from typing import List, Optional

from app.dependencies import get_current_user
from app.schemas.request import EventUpdateRequest, EventCreateRequest
from app.schemas.response import EventResponse
from config.database import get_db
from sqlalchemy.orm import Session
from app.models.models import Event, User
from datetime import date

event_router = APIRouter(
    prefix="/events",
    tags=['Events']
)

search_router = APIRouter(
    prefix="/search",
    tags=["Search/Filtering"]
)

@event_router.get("/all", response_model=List[EventResponse])
def get_all_events(session: Session = Depends(get_db), q:str = None):
    """Endpoint to get all events"""
    events = session.query(Event).all()
    return events

@event_router.get("/", response_model=List[EventResponse])
def get_events_for_user(current_user: User = Depends(get_current_user), session: Session = Depends(get_db)):
    """Endpoint to get all event created by this user"""
    events = session.query(Event).filter(Event.organiser == current_user.id).all()
    return events


@event_router.get("/{event_id}", response_model=EventResponse)
def get_single_event(event_id: str, current_user: User = Depends(get_current_user), session: Session = Depends(get_db)):
    """Endpoint to get a single event"""
    # First, fetch the event by ID
    event = session.query(Event).filter(Event.id == event_id).first()

    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    # Check if the current user is the organizer
    if event.organiser != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to view this event")

    return event

@event_router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(event_id: str, current_user: User = Depends(get_current_user), session: Session = Depends(get_db)):
    event = session.query(Event).filter(Event.uid == event_id).first()

    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    # Check if the current user is the organizer
    if event.organiser != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to view this event")

    session.delete(event)
    session.commit()
    return {"message": "Event deleted successfully"}

@event_router.post("/", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
def create_event(
    data: EventCreateRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_db)
):
    """Endpoint to create a new event"""
    event = Event(
        title=data.title,
        description=data.description,
        max_participants=data.max_participants,
        location=data.location,
        date=data.date,
        time=data.time,
        organiser=current_user.id
    )

    # Add the new event to the session and commit
    session.add(event)
    session.commit()
    session.refresh(event)

    return event

@event_router.put("/{event_id}", response_model=EventResponse)
def update_event(
    event_id: str,
    event_data: EventUpdateRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_db)
):
    """Endpoint to update an event"""
    # Fetch the event by event_id
    event = session.query(Event).filter(Event.id == event_id).first()

    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    # Check if the current user is the organizer
    if event.organiser != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to update this event")

    # Update the event's attributes only if they are provided in the request
    if event_data.title is not None:
        event.title = event_data.title
    if event_data.description is not None:
        event.description = event_data.description
    if event_data.max_participants is not None:
        event.max_participants = event_data.max_participants
    if event_data.location is not None:
        event.location = event_data.location
    if event_data.date is not None:
        event.date = event_data.date
    if event_data.time is not None:
        event.time = event_data.time

    # Commit the changes to the database
    session.commit()

    return event

@search_router.get("/", response_model=List[EventResponse])
def search_events(
            is_available: Optional[str] = None,
            location: Optional[str] = None,
            start_date: Optional[date] = None,
            end_date: Optional[date] = None,
            db: Session = Depends(get_db)
    ):
        query = db.query(Event)

        # Filter by category
        if is_available:
            query = query.filter(Event.is_available == is_available)

        # Filter by location
        if location:
            query = query.filter(Event.location == location)

        # Filter by date range
        if start_date and end_date:
            query = query.filter(Event.created_at.between(start_date, end_date))
        elif start_date:
            query = query.filter(Event.created_at >= start_date)
        elif end_date:
            query = query.filter(Event.created_at <= end_date)

        return query.all()