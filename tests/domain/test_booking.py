from datetime import datetime, timedelta
from decimal import Decimal
from uuid import uuid4

import pytest

from src.domain.aggregates.booking import Booking
from src.domain.events.booking_events import BookingExpired, BookingPaid, TicketReserved
from src.domain.events.ticket_events import TicketCheckedIn
from src.domain.exceptions.domain_exception import (
    BookingCannotExpireError,
    BookingPaymentDeadlinePassedError,
    IncorrectPaymentAmountError,
    InvalidTicketQuantityError,
    TicketCannotBeCheckedInError,
)
from src.domain.value_objects.booking_status import BookingStatus
from src.domain.value_objects.money import Money
from src.domain.value_objects.payment_deadline import PaymentDeadline
from src.domain.value_objects.ticket_code import TicketCode
from src.domain.value_objects.ticket_status import TicketStatus


def make_booking(quantity: int = 1, deadline_at: datetime | None = None) -> Booking:
    return Booking.create(
        customer_id=uuid4(),
        event_id=uuid4(),
        ticket_category_id=uuid4(),
        quantity=quantity,
        unit_price=Money(Decimal("100000")),
        payment_deadline=PaymentDeadline(deadline_at or datetime(2026, 7, 1, 12, 15)),
    )


def pay_booking(booking: Booking) -> None:
    ticket_codes = [TicketCode(f"TICKET-{index}") for index in range(booking.quantity)]
    booking.pay(
        amount=booking.total_price,
        paid_at=datetime(2026, 7, 1, 12, 0),
        ticket_codes=ticket_codes,
    )


def test_booking_cannot_be_created_with_zero_quantity():
    with pytest.raises(InvalidTicketQuantityError):
        make_booking(quantity=0)


def test_booking_creation_raises_ticket_reserved_domain_event():
    booking = make_booking(quantity=2)

    assert booking.status == BookingStatus.PENDING_PAYMENT
    assert any(isinstance(domain_event, TicketReserved) for domain_event in booking.domain_events)


def test_booking_total_price_includes_service_fee():
    booking = Booking.create(
        customer_id=uuid4(),
        event_id=uuid4(),
        ticket_category_id=uuid4(),
        quantity=2,
        unit_price=Money(Decimal("100000")),
        service_fee=Money(Decimal("5000")),
        payment_deadline=PaymentDeadline(datetime(2026, 7, 1, 12, 15)),
    )

    assert booking.total_price == Money(Decimal("205000"))


def test_booking_cannot_be_paid_after_payment_deadline():
    booking = make_booking(deadline_at=datetime(2026, 7, 1, 12, 15))

    with pytest.raises(BookingPaymentDeadlinePassedError):
        booking.pay(
            amount=booking.total_price,
            paid_at=datetime(2026, 7, 1, 12, 16),
            ticket_codes=[TicketCode("TICKET-1")],
        )


def test_booking_cannot_be_paid_with_incorrect_payment_amount():
    booking = make_booking()

    with pytest.raises(IncorrectPaymentAmountError):
        booking.pay(
            amount=Money(Decimal("1")),
            paid_at=datetime(2026, 7, 1, 12, 0),
            ticket_codes=[TicketCode("TICKET-1")],
        )


def test_paid_booking_cannot_expire():
    booking = make_booking()
    pay_booking(booking)

    with pytest.raises(BookingCannotExpireError):
        booking.expire(datetime(2026, 7, 1, 12, 30))


def test_pending_booking_can_expire_after_deadline():
    booking = make_booking(deadline_at=datetime(2026, 7, 1, 12, 15))

    booking.expire(datetime(2026, 7, 1, 12, 16))

    assert booking.status == BookingStatus.EXPIRED
    assert any(isinstance(domain_event, BookingExpired) for domain_event in booking.domain_events)


def test_paid_booking_issues_tickets_and_raises_booking_paid_event():
    booking = make_booking(quantity=2)

    pay_booking(booking)

    assert booking.status == BookingStatus.PAID
    assert len(booking.tickets) == 2
    assert all(ticket.status == TicketStatus.ACTIVE for ticket in booking.tickets)
    assert any(isinstance(domain_event, BookingPaid) for domain_event in booking.domain_events)


def test_checked_in_ticket_cannot_be_checked_in_again():
    booking = make_booking()
    pay_booking(booking)

    booking.check_in_ticket(TicketCode("TICKET-0"), datetime(2026, 7, 20, 9, 0))

    with pytest.raises(TicketCannotBeCheckedInError):
        booking.check_in_ticket(TicketCode("TICKET-0"), datetime(2026, 7, 20, 9, 5))


def test_check_in_raises_ticket_checked_in_domain_event():
    booking = make_booking()
    pay_booking(booking)

    booking.check_in_ticket(TicketCode("TICKET-0"), datetime(2026, 7, 20, 9, 0))

    assert booking.has_checked_in_ticket() is True
    assert any(isinstance(domain_event, TicketCheckedIn) for domain_event in booking.domain_events)
