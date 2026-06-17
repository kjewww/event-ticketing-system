from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class TicketCategorySalesResponse(BaseModel):
    ticket_category_id: UUID
    ticket_category_name: str
    tickets_sold: int


class BookingStatusCountResponse(BaseModel):
    status: str
    count: int


class EventSalesReportResponse(BaseModel):
    event_id: UUID
    tickets_sold_per_category: list[TicketCategorySalesResponse]
    booking_status_counts: list[BookingStatusCountResponse]
    total_revenue_amount: Decimal
    currency: str


class EventParticipantResponse(BaseModel):
    customer_id: UUID
    customer_name: str
    ticket_category_name: str
    ticket_code: str
    check_in_status: str