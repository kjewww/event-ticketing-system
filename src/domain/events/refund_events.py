from datetime import datetime, timezone
from uuid import UUID, uuid4


class RefundRequested:
    def __init__(
        self,
        refund_id: UUID,
        booking_id: UUID,
    ):
        self.id = uuid4()
        self.occurred_at = datetime.now(timezone.utc)

        self.refund_id = refund_id
        self.booking_id = booking_id


class RefundApproved:
    def __init__(
        self,
        refund_id: UUID,
        booking_id: UUID,
    ):
        self.id = uuid4()
        self.occurred_at = datetime.now(timezone.utc)

        self.refund_id = refund_id
        self.booking_id = booking_id


class RefundRejected:
    def __init__(
        self,
        refund_id: UUID,
        booking_id: UUID,
        reason: str,
    ):
        self.id = uuid4()
        self.occurred_at = datetime.now(timezone.utc)

        self.refund_id = refund_id
        self.booking_id = booking_id
        self.reason = reason


class RefundPaidOut:
    def __init__(
        self,
        refund_id: UUID,
        booking_id: UUID,
        payment_reference: str,
    ):
        self.id = uuid4()
        self.occurred_at = datetime.now(timezone.utc)

        self.refund_id = refund_id
        self.booking_id = booking_id
        self.payment_reference = payment_reference