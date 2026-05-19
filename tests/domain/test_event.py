from datetime import date
from decimal import Decimal

import pytest

from src.domain.aggregates.event import Event
from src.domain.entities.ticket_category import TicketCategory
from src.domain.events.event_created import EventCreated
from src.domain.events.event_published import EventPublished
from src.domain.events.ticket_category_created import TicketCategoryCreated
from src.domain.exceptions.domain_exception import (
    EventCannotBePublishedError,
    EventTicketCategoryQuotaExceededError,
    InvalidEventCapacityError,
)
from src.domain.value_objects.date_range import DateRange
from src.domain.value_objects.event_status import EventStatus
from src.domain.value_objects.money import Money


def make_event(capacity: int = 100) -> Event:
    return Event(
        organizer_id="organizer-1",
        name="Tech Conference",
        description="Annual technology conference",
        date_range=DateRange(date(2026, 7, 20), date(2026, 7, 20)),
        location="Surabaya",
        capacity=capacity,
    )


def make_ticket_category(quota: int = 50) -> TicketCategory:
    return TicketCategory(
        name="Regular",
        price=Money(Decimal("100000")),
        quota=quota,
        sales_date_range=DateRange(date(2026, 6, 1), date(2026, 7, 20)),
    )


def test_event_cannot_be_created_with_invalid_schedule():
    with pytest.raises(ValueError):
        DateRange(date(2026, 7, 21), date(2026, 7, 20))


def test_event_cannot_be_created_with_zero_or_negative_capacity():
    with pytest.raises(InvalidEventCapacityError):
        make_event(capacity=0)

    with pytest.raises(InvalidEventCapacityError):
        make_event(capacity=-1)


def test_new_event_has_draft_status_and_event_created_domain_event():
    event = make_event()

    assert event.status == EventStatus.DRAFT
    assert any(isinstance(domain_event, EventCreated) for domain_event in event.domain_events)


def test_event_cannot_be_published_without_active_ticket_category():
    event = make_event()

    with pytest.raises(EventCannotBePublishedError):
        event.publish()


def test_ticket_category_quota_cannot_exceed_event_capacity():
    event = make_event(capacity=10)
    category = make_ticket_category(quota=11)

    with pytest.raises(EventTicketCategoryQuotaExceededError):
        event.add_ticket_category(category)


def test_add_ticket_category_raises_domain_event():
    event = make_event(capacity=100)
    category = make_ticket_category(quota=50)

    event.add_ticket_category(category)

    assert category in event.ticket_categories
    assert any(
        isinstance(domain_event, TicketCategoryCreated)
        and domain_event.event_id == event.id
        and domain_event.ticket_category_id == category.id
        for domain_event in event.domain_events
    )


def test_event_can_be_published_with_active_ticket_category():
    event = make_event()
    event.add_ticket_category(make_ticket_category())

    event.publish()

    assert event.status == EventStatus.PUBLISHED
    assert any(isinstance(domain_event, EventPublished) for domain_event in event.domain_events)
