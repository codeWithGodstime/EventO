from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class UserLoginRequest(BaseModel):
    email:EmailStr
    password:str


class UserRegisterRequest(BaseModel):
    email:EmailStr
    username:str
    password:str
    # phone_number: str = None


class EventUpdateRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    max_participants: Optional[int] = None
    location: Optional[str] = None
    date: Optional[date] = None
    time: Optional[str] = None


class EventCreateRequest(BaseModel):
    title: str
    description: str
    max_participants: int
    location: str
    date: str
    time: str


class TicketCreateRequest(BaseModel):
    expiration_date: str
    price:float


class TicketPurchaseRequest(BaseModel):
    purchaser_email:EmailStr
    ticket: str
