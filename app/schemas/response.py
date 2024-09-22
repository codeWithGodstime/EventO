from datetime import datetime, date, time

from pydantic import BaseModel, ConfigDict

class BaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


class UserResponse(BaseResponse):
    uid: str
    username:str
    email:str
    phone_number:str | None
    is_organizer:bool
    is_active:bool


class UserLoginReponse(BaseResponse):
    access: str
    refresh: str
    data : UserResponse

class EventResponse(BaseResponse):
    title: str
    description: str
    max_participants: int
    location: str
    date: date
    time: time
    organiser: UserResponse


class TicketResponse(BaseResponse):
    expiration_date:date
    price: float
    is_available:bool
    # event: EventResponse


class TicketPurchasedResponse(BaseResponse):
    purchaser_email:str
    # ticket:TicketResponse

