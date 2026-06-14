from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class PurchasedTicketResponse(BaseModel):
    ticket_id: UUID
    booking_id: UUID
    event_id: UUID
    event_name: str
    ticket_category_id: UUID
    ticket_category_name: str
    ticket_code: str
    status: str
    checked_in_at: datetime | None


class CheckInTicketRequest(BaseModel):
    event_id: UUID
    ticket_code: str
    checked_in_at: datetime | None = None


class CheckInTicketResponse(BaseModel):
    ticket_code: str
    event_id: UUID
    booking_id: UUID
    status: str
    checked_in_at: datetime | None