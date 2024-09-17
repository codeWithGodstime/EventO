from sqlalchemy import Column, String, Boolean, Integer, Date, Time, ForeignKey, Float
from sqlalchemy.orm import relationship
from .base import ModelBase
from config.database import Base


class User(Base, ModelBase):
    __tablename__ = "users"

    is_active = Column(Boolean, default=False)  # Changed default to False
    is_verified = Column(Boolean, default=False)  # Changed default to False
    is_admin = Column(Boolean, default=False)
    is_organizer = Column(Boolean, default=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    phone_number = Column(String(20), nullable=True)

    events = relationship("Event", back_populates="user")

    def save(self):
        pass


class Event(Base, ModelBase):
    __tablename__ = "events"

    title = Column(String, nullable=False)
    description = Column(String(20), nullable=False)
    max_participants = Column(Integer)
    location = Column(String(60))
    date = Column(Date, nullable=False)
    time = Column(Time)
    organiser = Column(Integer, ForeignKey("users.id"))  # Fixed foreign key

    user = relationship("User", back_populates="events")
    tickets = relationship("Tickets", back_populates="ticket_event")  # Fixed relationship

    def save(self):
        pass


class Tickets(Base, ModelBase):
    __tablename__ = "tickets"

    is_available = Column(Boolean, default=True)
    expiration_date = Column(Date)
    # type = Column() # TODO: add this field later
    price = Column(Float, default=0.00, nullable=True)  # Simplified price field
    event = Column(Integer, ForeignKey("events.id"))  # Fixed foreign key

    ticket_event = relationship("Event", back_populates="tickets")
    sold_tickets = relationship("TicketPurchase", back_populates="ticket_purchased")

    def save(self):
        pass


class TicketPurchase(Base, ModelBase):
    __tablename__ = "ticket_purchases"

    purchaser_email = Column(String, nullable=False)
    ticket = Column(Integer, ForeignKey("tickets.id"))  # Fixed foreign key

    ticket_purchased = relationship("Tickets", back_populates="sold_tickets")

    def save(self):
        pass

