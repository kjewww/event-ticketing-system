from datetime import datetime, timezone
from uuid import UUID, uuid4

from src.domain.value_objects.money import Money


class RefundRequested:
    def __init__(
        self,
        refund_id: UUID,
        booking_id: UUID,
        customer_id: UUID,
        amount: Money,
    ):
        self.id = uuid4()
        self.occurred_at = datetime.now(timezone.utc)

        self.refund_id = refund_id
        self.booking_id = booking_id
        self.customer_id = customer_id
        self.amount = amount


class RefundApproved:
    def __init__(
        self,
        refund_id: UUID,
        booking_id: UUID,
        customer_id: UUID,
        amount: Money,
    ):
        self.id = uuid4()
        self.occurred_at = datetime.now(timezone.utc)

        self.refund_id = refund_id
        self.booking_id = booking_id
        self.customer_id = customer_id
        self.amount = amount


class RefundRejected:
    def __init__(
        self,
        refund_id: UUID,
        booking_id: UUID,
        customer_id: UUID,
        rejection_reason: str,
    ):
        self.id = uuid4()
        self.occurred_at = datetime.now(timezone.utc)

        self.refund_id = refund_id
        self.booking_id = booking_id
        self.customer_id = customer_id
        self.rejection_reason = rejection_reason


class RefundPaidOut:
    def __init__(
        self,
        refund_id: UUID,
        booking_id: UUID,
        customer_id: UUID,
        payment_reference: str,
    ):
        self.id = uuid4()
        self.occurred_at = datetime.now(timezone.utc)

        self.refund_id = refund_id
        self.booking_id = booking_id
        self.customer_id = customer_id
        self.payment_reference = payment_reference