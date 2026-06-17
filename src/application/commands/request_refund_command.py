from datetime import datetime
from uuid import UUID


class RequestRefundCommand:
    def __init__(
        self,
        booking_id: UUID,
        customer_id: UUID,
        reason: str | None,
        requested_at: datetime,
        refund_deadline: datetime,
    ):
        self.booking_id = booking_id
        self.customer_id = customer_id
        self.reason = reason
        self.requested_at = requested_at
        self.refund_deadline = refund_deadline