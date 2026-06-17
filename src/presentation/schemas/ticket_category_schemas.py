from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class CreateTicketCategoryRequest(BaseModel):
    organizer_id: UUID
    name: str
    price_amount: Decimal
    currency: str = "IDR"
    quota: int
    sales_start_date: date
    sales_end_date: date


class TicketCategoryResponse(BaseModel):
    event_id: UUID
    ticket_category_id: UUID
    name: str
    price_amount: Decimal
    currency: str
    quota: int
    sales_start_date: date
    sales_end_date: date
    is_active: bool


class DisableTicketCategoryRequest(BaseModel):
    organizer_id: UUID


class DisableTicketCategoryResponse(BaseModel):
    event_id: UUID
    ticket_category_id: UUID
    name: str
    is_active: bool