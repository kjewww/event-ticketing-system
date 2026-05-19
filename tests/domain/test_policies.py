from datetime import date, datetime
from decimal import Decimal
from uuid import uuid4

import pytest

from src.domain.aggregates.booking import Booking
from src.domain.aggregates.event import Event
from src.domain.entities.ticket_category import TicketCategory
from src.domain.exceptions.domain_exception import BookingNotAllowedError, RefundNotAllowedError
from src.domain.services.booking_policy import BookingPolicy
from src.domain.services.event_cancellation_service import EventCancellationService
from src.domain.services.refund_policy import RefundPolicy
from src.domain.value_objects.booking_status import BookingStatus
from src.domain.value_objects.date_range import DateRange
from src.domain.value_objects.event_status import EventStatus
from src.domain.value_objects.money import Money
from src.domain.value_objects.payment_deadline import PaymentDeadline
from src.domain.value_objects.ticket_code import TicketCode
from src.domain.value_objects.ticket_status import TicketStatus


def make_category() -> TicketCategory:
    return TicketCategory(
        name="Regular",
        price=Money(Decimal("100000")),
        quota=10,
        sales_date_range=DateRange(date(2026, 6, 1), date(2026, 7, 20)),
    )


def make_booking(status: BookingStatus = BookingStatus.PAID) -> Booking:
    return Booking(
        id=uuid4(),
        customer_id=uuid4(),
        event_id=uuid4(),
        ticket_category_id=uuid4(),
        quantity=1,
        unit_price=Money(Decimal("100000")),
        payment_deadline=PaymentDeadline(datetime(2026, 7, 1, 12, 15)),
        status=status,
    )


def test_booking_policy_rejects_unpublished_event():
    policy = BookingPolicy()

    with pytest.raises(BookingNotAllowedError):
        policy.ensure_booking_allowed(
            event_status=EventStatus.DRAFT,
            ticket_category=make_category(),
            quantity=1,
            remaining_quota=10,
            has_active_booking_for_event=False,
            requested_at=datetime(2026, 6, 10, 10, 0),
        )


def test_booking_policy_accepts_valid_booking_request():
    policy = BookingPolicy()

    policy.ensure_booking_allowed(
        event_status=EventStatus.PUBLISHED,
        ticket_category=make_category(),
        quantity=1,
        remaining_quota=10,
        has_active_booking_for_event=False,
        requested_at=datetime(2026, 6, 10, 10, 0),
    )


def test_booking_policy_rejects_inactive_ticket_category():
    category = make_category()
    category.disable()
    policy = BookingPolicy()

    with pytest.raises(BookingNotAllowedError):
        policy.ensure_booking_allowed(
            event_status=EventStatus.PUBLISHED,
            ticket_category=category,
            quantity=1,
            remaining_quota=10,
            has_active_booking_for_event=False,
            requested_at=datetime(2026, 6, 10, 10, 0),
        )


def test_booking_policy_rejects_quantity_exceeding_remaining_quota():
    policy = BookingPolicy()

    with pytest.raises(BookingNotAllowedError):
        policy.ensure_booking_allowed(
            event_status=EventStatus.PUBLISHED,
            ticket_category=make_category(),
            quantity=11,
            remaining_quota=10,
            has_active_booking_for_event=False,
            requested_at=datetime(2026, 6, 10, 10, 0),
        )


def test_refund_policy_rejects_refund_if_ticket_has_been_checked_in():
    booking = Booking.create(
        customer_id=uuid4(),
        event_id=uuid4(),
        ticket_category_id=uuid4(),
        quantity=1,
        unit_price=Money(Decimal("100000")),
        payment_deadline=PaymentDeadline(datetime(2026, 7, 1, 12, 15)),
    )
    booking.pay(
        amount=booking.total_price,
        paid_at=datetime(2026, 7, 1, 12, 0),
        ticket_codes=[TicketCode("TICKET-1")],
    )
    booking.check_in_ticket(TicketCode("TICKET-1"), datetime(2026, 7, 20, 9, 0))

    with pytest.raises(RefundNotAllowedError):
        RefundPolicy().ensure_refund_allowed(
            booking=booking,
            event_status=EventStatus.PUBLISHED,
            refund_deadline=datetime(2026, 7, 19, 23, 59),
            requested_at=datetime(2026, 7, 10, 10, 0),
        )


def test_refund_policy_accepts_cancelled_event_refund_before_deadline_rule_check():
    booking = make_booking(status=BookingStatus.PAID)

    RefundPolicy().ensure_refund_allowed(
        booking=booking,
        event_status=EventStatus.CANCELLED,
        refund_deadline=datetime(2026, 7, 1, 0, 0),
        requested_at=datetime(2026, 7, 10, 10, 0),
    )


def test_event_cancellation_service_marks_paid_bookings_as_refund_required():
    event = Event(
        organizer_id="organizer-1",
        name="Tech Conference",
        description="Annual technology conference",
        date_range=DateRange(date(2026, 7, 20), date(2026, 7, 20)),
        location="Surabaya",
        capacity=10,
    )
    event.add_ticket_category(make_category())
    event.publish()

    booking = make_booking(status=BookingStatus.PAID)
    booking.tickets.append(
        __import__("src.domain.entities.ticket", fromlist=["Ticket"]).Ticket(
            id=uuid4(),
            booking_id=booking.id,
            event_id=booking.event_id,
            ticket_category_id=booking.ticket_category_id,
            ticket_code=TicketCode("TICKET-1"),
            status=TicketStatus.ACTIVE,
        )
    )

    EventCancellationService().cancel_event_and_mark_paid_bookings(
        event=event,
        paid_bookings=[booking],
    )

    assert event.status == EventStatus.CANCELLED
    assert booking.refund_required is True
    assert booking.tickets[0].status == TicketStatus.REFUND_REQUIRED
