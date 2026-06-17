from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class CreateEventRequest(BaseModel):
    organizer_id: UUID
    name: str
    description: str
    start_date: date
    end_date: date
    location: str
    capacity: int


class EventResponse(BaseModel):
    event_id: UUID
    organizer_id: UUID
    name: str
    description: str
    start_date: date
    end_date: date
    location: str
    capacity: int
    status: str


class OrganizerActionRequest(BaseModel):
    organizer_id: UUID


class EventStatusResponse(BaseModel):
    event_id: UUID
    name: str
    status: str


class AvailableEventResponse(BaseModel):
    event_id: UUID
    name: str
    start_date: date
    end_date: date
    location: str
    lowest_ticket_price: Decimal


class EventTicketCategoryResponse(BaseModel):
    ticket_category_id: UUID
    name: str
    price_amount: Decimal
    currency: str
    quota: int
    remaining_quota: int
    sales_start_date: date
    sales_end_date: date
    is_active: bool
    purchase_status: str


class EventDetailsResponse(BaseModel):
    event_id: UUID
    name: str
    description: str
    start_date: date
    end_date: date
    location: str
    organizer_id: UUID
    status: str
    ticket_categories: list[EventTicketCategoryResponse]