from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class RequestRefundRequest(BaseModel):
    customer_id: UUID
    reason: str | None = None
    requested_at: datetime | None = None
    refund_deadline: datetime


class RequestRefundResponse(BaseModel):
    refund_id: UUID
    booking_id: UUID
    customer_id: UUID
    amount: Decimal
    currency: str
    status: str
    reason: str | None


class ApproveRefundRequest(BaseModel):
    organizer_id: UUID


class ApproveRefundResponse(BaseModel):
    refund_id: UUID
    booking_id: UUID
    status: str


class RejectRefundRequest(BaseModel):
    organizer_id: UUID
    rejection_reason: str


class RejectRefundResponse(BaseModel):
    refund_id: UUID
    booking_id: UUID
    status: str
    rejection_reason: str


class MarkRefundPaidOutRequest(BaseModel):
    admin_id: UUID


class MarkRefundPaidOutResponse(BaseModel):
    refund_id: UUID
    booking_id: UUID
    status: str
    payment_reference: str