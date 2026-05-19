from decimal import Decimal
from uuid import uuid4

import pytest

from src.domain.aggregates.refund import Refund
from src.domain.events.refund_events import RefundApproved, RefundPaidOut, RefundRejected, RefundRequested
from src.domain.exceptions.domain_exception import (
    PaymentReferenceRequiredError,
    RefundStatusError,
    RejectionReasonRequiredError,
)
from src.domain.value_objects.money import Money
from src.domain.value_objects.refund_status import RefundStatus


def make_refund() -> Refund:
    return Refund.request(
        booking_id=uuid4(),
        customer_id=uuid4(),
        amount=Money(Decimal("100000")),
        reason="Customer request",
    )


def test_refund_request_sets_requested_status_and_raises_domain_event():
    refund = make_refund()

    assert refund.status == RefundStatus.REQUESTED
    assert any(isinstance(domain_event, RefundRequested) for domain_event in refund.domain_events)


def test_refund_cannot_be_approved_if_not_requested():
    refund = make_refund()
    refund.approve()

    with pytest.raises(RefundStatusError):
        refund.approve()


def test_refund_approval_changes_status_and_raises_domain_event():
    refund = make_refund()

    refund.approve()

    assert refund.status == RefundStatus.APPROVED
    assert any(isinstance(domain_event, RefundApproved) for domain_event in refund.domain_events)


def test_rejected_refund_must_have_rejection_reason():
    refund = make_refund()

    with pytest.raises(RejectionReasonRequiredError):
        refund.reject("   ")


def test_refund_rejection_changes_status_and_raises_domain_event():
    refund = make_refund()

    refund.reject("Outside refund period")

    assert refund.status == RefundStatus.REJECTED
    assert refund.rejection_reason == "Outside refund period"
    assert any(isinstance(domain_event, RefundRejected) for domain_event in refund.domain_events)


def test_approved_refund_can_be_marked_paid_out():
    refund = make_refund()
    refund.approve()

    refund.mark_paid_out("BANK-REF-001")

    assert refund.status == RefundStatus.PAID_OUT
    assert refund.payment_reference == "BANK-REF-001"
    assert any(isinstance(domain_event, RefundPaidOut) for domain_event in refund.domain_events)


def test_refund_paid_out_requires_payment_reference():
    refund = make_refund()
    refund.approve()

    with pytest.raises(PaymentReferenceRequiredError):
        refund.mark_paid_out("   ")
