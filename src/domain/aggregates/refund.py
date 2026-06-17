from uuid import UUID, uuid4

from src.domain.events.refund_events import (
    RefundApproved,
    RefundPaidOut,
    RefundRejected,
    RefundRequested,
)
from src.domain.exceptions.domain_exception import (
    PaymentReferenceRequiredError,
    RefundStatusError,
    RejectionReasonRequiredError,
)
from src.domain.value_objects.money import Money
from src.domain.value_objects.refund_status import RefundStatus


class Refund:
    def __init__(
        self,
        id: UUID,
        booking_id: UUID,
        customer_id: UUID,
        amount: Money,
        reason: str | None = None,
        status: RefundStatus = RefundStatus.REQUESTED,
        rejection_reason: str | None = None,
        payment_reference: str | None = None,
    ):
        self.id = id
        self.booking_id = booking_id
        self.customer_id = customer_id
        self.amount = amount
        self.reason = reason
        self.status = status
        self.rejection_reason = rejection_reason
        self.payment_reference = payment_reference
        self._domain_events: list[object] = []

    @classmethod
    def request(
        cls,
        booking_id: UUID,
        customer_id: UUID,
        amount: Money,
        reason: str | None = None,
    ) -> "Refund":
        refund = cls(
            id=uuid4(),
            booking_id=booking_id,
            customer_id=customer_id,
            amount=amount,
            reason=reason,
            status=RefundStatus.REQUESTED,
        )

        refund._domain_events.append(
            RefundRequested(
                refund_id=refund.id,
                booking_id=refund.booking_id,
                customer_id=refund.customer_id,
                amount=refund.amount,
            )
        )

        return refund

    @classmethod
    def reconstruct(
        cls,
        id: UUID,
        booking_id: UUID,
        customer_id: UUID,
        amount: Money,
        reason: str | None,
        status: RefundStatus,
        rejection_reason: str | None = None,
        payment_reference: str | None = None,
    ) -> "Refund":
        return cls(
            id=id,
            booking_id=booking_id,
            customer_id=customer_id,
            amount=amount,
            reason=reason,
            status=status,
            rejection_reason=rejection_reason,
            payment_reference=payment_reference,
        )

    def approve(self) -> None:
        if self.status != RefundStatus.REQUESTED:
            raise RefundStatusError("Only requested refunds can be approved.")

        self.status = RefundStatus.APPROVED

        self._domain_events.append(
            RefundApproved(
                refund_id=self.id,
                booking_id=self.booking_id,
                customer_id=self.customer_id,
                amount=self.amount,
            )
        )

    def reject(self, reason: str) -> None:
        if self.status != RefundStatus.REQUESTED:
            raise RefundStatusError("Only requested refunds can be rejected.")

        if not reason or not reason.strip():
            raise RejectionReasonRequiredError("Rejection reason is required.")

        self.status = RefundStatus.REJECTED
        self.rejection_reason = reason

        self._domain_events.append(
            RefundRejected(
                refund_id=self.id,
                booking_id=self.booking_id,
                customer_id=self.customer_id,
                rejection_reason=self.rejection_reason,
            )
        )

    def mark_paid_out(self, payment_reference: str) -> None:
        if self.status != RefundStatus.APPROVED:
            raise RefundStatusError("Only approved refunds can be marked as paid out.")

        if not payment_reference or not payment_reference.strip():
            raise PaymentReferenceRequiredError("Payment reference is required.")

        self.status = RefundStatus.PAID_OUT
        self.payment_reference = payment_reference

        self._domain_events.append(
            RefundPaidOut(
                refund_id=self.id,
                booking_id=self.booking_id,
                customer_id=self.customer_id,
                payment_reference=self.payment_reference,
            )
        )

    @property
    def domain_events(self):
        return list(self._domain_events)

    def clear_domain_events(self) -> None:
        self._domain_events.clear()