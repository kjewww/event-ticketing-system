from datetime import date
from decimal import Decimal

import pytest

from src.domain.aggregates.event import Event

from src.domain.entities.ticket_category import TicketCategory

from src.domain.value_objects.date_range import DateRange
from src.domain.value_objects.money import Money
from src.domain.value_objects.event_status import EventStatus

from src.domain.events.event_created import EventCreated
from src.domain.events.event_published import EventPublished
from src.domain.events.event_cancelled import EventCancelled


def create_valid_event():

    return Event(
        name="Music Festival",
        description="Annual music festival",
        date_range=DateRange(
            date(2026, 6, 10),
            date(2026, 6, 12)
        ),
        location="Surabaya",
        capacity=100
    )


def create_valid_ticket_category():

    return TicketCategory(
        name="VIP",
        price=Money(Decimal("100000")),
        quota=10,
        sales_date_range=DateRange(
            date(2026, 5, 1),
            date(2026, 6, 1)
        )
    )


# ==================================================
# UC1 - Create Event
# ==================================================

def test_event_cannot_be_created_with_invalid_schedule():

    with pytest.raises(ValueError):

        Event(
            name="Invalid Event",
            description="Invalid",
            date_range=DateRange(
                date(2026, 6, 10),
                date(2026, 6, 1)
            ),
            location="Surabaya",
            capacity=100
        )


def test_event_cannot_be_created_with_zero_capacity():

    with pytest.raises(ValueError):

        Event(
            name="Invalid Event",
            description="Invalid",
            date_range=DateRange(
                date(2026, 6, 1),
                date(2026, 6, 10)
            ),
            location="Surabaya",
            capacity=0
        )


def test_new_event_should_have_draft_status():

    event = create_valid_event()

    assert event.status == EventStatus.DRAFT


def test_event_created_should_raise_domain_event():

    event = create_valid_event()

    assert isinstance(
        event.domain_events[0],
        EventCreated
    )


# ==================================================
# UC2 - Publish Event
# ==================================================

def test_event_cannot_be_published_without_ticket_category():

    event = create_valid_event()

    with pytest.raises(ValueError):
        event.publish()


def test_event_can_be_published():

    event = create_valid_event()

    category = create_valid_ticket_category()

    event.add_ticket_category(category)

    event.publish()

    assert event.status == EventStatus.PUBLISHED


def test_event_published_should_raise_domain_event():

    event = create_valid_event()

    category = create_valid_ticket_category()

    event.add_ticket_category(category)

    event.publish()

    assert isinstance(
        event.domain_events[-1],
        EventPublished
    )


# ==================================================
# UC3 - Cancel Event
# ==================================================

def test_only_published_event_can_be_cancelled():

    event = create_valid_event()

    with pytest.raises(ValueError):
        event.cancel()


def test_cancel_event_should_disable_ticket_categories():

    event = create_valid_event()

    category = create_valid_ticket_category()

    event.add_ticket_category(category)

    event.publish()

    event.cancel()

    assert category.is_active is False


def test_event_cancelled_should_raise_domain_event():

    event = create_valid_event()

    category = create_valid_ticket_category()

    event.add_ticket_category(category)

    event.publish()

    event.cancel()

    assert isinstance(
        event.domain_events[-1],
        EventCancelled
    )


# ==================================================
# UC4 - Ticket Category
# ==================================================

def test_ticket_category_quota_cannot_exceed_event_capacity():

    event = create_valid_event()

    category = TicketCategory(
        name="VIP",
        price=Money(Decimal("100000")),
        quota=200,
        sales_date_range=DateRange(
            date(2026, 5, 1),
            date(2026, 6, 1)
        )
    )

    with pytest.raises(ValueError):
        event.add_ticket_category(category)


def test_ticket_sales_period_must_end_before_event_starts():

    event = create_valid_event()

    category = TicketCategory(
        name="VIP",
        price=Money(Decimal("100000")),
        quota=10,
        sales_date_range=DateRange(
            date(2026, 5, 1),
            date(2026, 6, 11)
        )
    )

    with pytest.raises(ValueError):
        event.add_ticket_category(category)