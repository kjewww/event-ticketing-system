from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class CreateBookingRequest(BaseModel):
    customer_id: UUID
    customer_name: str
    event_id: UUID
    ticket_category_id: UUID
    quantity: int
    requested_at: datetime | None = None
    service_fee_amount: Decimal = Decimal("0")
    currency: str = "IDR"


class CreateBookingResponse(BaseModel):
    booking_id: UUID
    customer_id: UUID
    event_id: UUID
    ticket_category_id: UUID
    quantity: int
    total_price_amount: Decimal
    currency: str
    payment_deadline_at: datetime
    status: str


class PayBookingRequest(BaseModel):
    customer_id: UUID
    amount: Decimal
    paid_at: datetime | None = None
    currency: str = "IDR"


class PayBookingResponse(BaseModel):
    booking_id: UUID
    status: str
    total_price_amount: Decimal
    currency: str
    ticket_codes: list[str]
    payment_reference: str


class ExpireBookingRequest(BaseModel):
    now: datetime | None = None


class ExpireBookingResponse(BaseModel):
    booking_id: UUID
    status: str