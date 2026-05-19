import pytest
from decimal import Decimal
from datetime import datetime, timedelta

from src.domain.aggregates.event import Event
from src.domain.entities.ticket_category import TicketCategory
from src.domain.value_objects.date_range import DateRange
from src.domain.value_objects.money import Money
from src.domain.value_objects.event_status import EventStatus


# ─────────────────────────────────────────
# HELPERS / FIXTURES
# ─────────────────────────────────────────

NOW = datetime(2025, 1, 1, 0, 0, 0)

def make_event_date_range() -> DateRange:
    """Event berlangsung 10–11 Februari 2025."""
    return DateRange(
        start_date=datetime(2025, 2, 10),
        end_date=datetime(2025, 2, 11),
    )

def make_event(**kwargs) -> Event:
    defaults = dict(
        organizer_id="org-1",
        name="PyCon Surabaya",
        description="Python conference",
        date_range=make_event_date_range(),
        location="Surabaya",
        capacity=100,
    )
    defaults.update(kwargs)
    return Event(**defaults)

def make_category(
    quota: int = 50,
    price: Decimal = Decimal("100000"),
    sales_start: datetime = datetime(2025, 1, 1),
    sales_end: datetime = datetime(2025, 2, 9),   # sebelum event start
) -> TicketCategory:
    return TicketCategory(
        name="Regular",
        price=Money(price),
        quota=quota,
        sales_date_range=DateRange(sales_start, sales_end),
    )


# ─────────────────────────────────────────
# US:1 — CREATE EVENT
# ─────────────────────────────────────────

class TestCreateEvent:

    def test_create_event_successfully(self):
        """US:1 — event berhasil dibuat dengan data yang valid."""
        event = make_event()
        assert event.name == "PyCon Surabaya"
        assert event.location == "Surabaya"
        assert event.capacity == 100

    def test_new_event_status_is_draft(self):
        """US:1 — AC: status event baru harus DRAFT."""
        event = make_event()
        assert event.status == EventStatus.DRAFT

    def test_raises_if_capacity_is_zero(self):
        """US:1 — AC: capacity tidak boleh <= 0."""
        with pytest.raises(ValueError):
            make_event(capacity=0)

    def test_raises_if_capacity_is_negative(self):
        """US:1 — AC: capacity tidak boleh <= 0."""
        with pytest.raises(ValueError):
            make_event(capacity=-1)

    def test_raises_if_end_date_before_start_date(self):
        """US:1 — AC: end date tidak boleh lebih awal dari start date."""
        with pytest.raises(ValueError):
            make_event(date_range=DateRange(
                start_date=datetime(2025, 2, 10),
                end_date=datetime(2025, 2, 5),   # lebih awal
            ))

    def test_raises_if_end_date_equals_start_date(self):
        """US:1 — AC: end date tidak boleh sama dengan start date."""
        with pytest.raises(ValueError):
            make_event(date_range=DateRange(
                start_date=datetime(2025, 2, 10),
                end_date=datetime(2025, 2, 10),
            ))

    def test_records_event_created_domain_event(self):
        """US:1 — AC: sistem memunculkan domain event EventCreated."""
        from src.domain.events.event_created import EventCreated
        event = make_event()
        types = [type(e) for e in event.domain_events]
        assert EventCreated in types


# ─────────────────────────────────────────
# US:2 — PUBLISH EVENT
# ─────────────────────────────────────────

class TestPublishEvent:

    def test_publish_draft_event_successfully(self):
        """US:2 — AC: event Draft dengan kategori aktif bisa dipublish."""
        event = make_event()
        event.add_ticket_category(make_category())
        event.publish()
        assert event.status == EventStatus.PUBLISHED

    def test_raises_if_no_ticket_category(self):
        """US:2 — AC: tidak bisa publish tanpa ticket category."""
        event = make_event()
        with pytest.raises(ValueError):
            event.publish()

    def test_raises_if_all_categories_inactive(self):
        """US:2 — AC: harus ada minimal 1 kategori aktif."""
        event = make_event()
        category = make_category()
        event.add_ticket_category(category)
        category.disable()   # nonaktifkan satu-satunya kategori
        with pytest.raises(ValueError):
            event.publish()

    def test_raises_if_event_already_published(self):
        """US:2 — AC: hanya event Draft yang bisa dipublish."""
        event = make_event()
        event.add_ticket_category(make_category())
        event.publish()
        with pytest.raises(ValueError):
            event.publish()   # publish kedua kali

    def test_raises_if_event_is_cancelled(self):
        """US:2 — AC: event Cancelled tidak bisa dipublish."""
        event = make_event()
        event.add_ticket_category(make_category())
        event.publish()
        event.cancel()
        with pytest.raises(ValueError):
            event.publish()

    def test_records_event_published_domain_event(self):
        """US:2 — AC: sistem memunculkan domain event EventPublished."""
        from src.domain.events.event_published import EventPublished
        event = make_event()
        event.add_ticket_category(make_category())
        event.publish()
        types = [type(e) for e in event.domain_events]
        assert EventPublished in types


# ─────────────────────────────────────────
# US:3 — CANCEL EVENT
# ─────────────────────────────────────────

class TestCancelEvent:

    def test_cancel_published_event_successfully(self):
        """US:3 — AC: event Published bisa di-cancel."""
        event = make_event()
        event.add_ticket_category(make_category())
        event.publish()
        event.cancel()
        assert event.status == EventStatus.CANCELLED

    def test_raises_if_event_is_draft(self):
        """US:3 — AC: hanya event Published yang bisa di-cancel."""
        event = make_event()
        with pytest.raises(ValueError):
            event.cancel()

    def test_raises_if_event_is_completed(self):
        """US:3 — AC: event Completed tidak bisa di-cancel."""
        event = make_event()
        event.add_ticket_category(make_category())
        event.publish()
        event.status = EventStatus.COMPLETED   # simulasi completed
        with pytest.raises(ValueError):
            event.cancel()

    def test_all_ticket_categories_disabled_on_cancel(self):
        """US:3 — AC: semua ticket category tidak bisa dibeli setelah event di-cancel."""
        event = make_event()
        event.add_ticket_category(make_category(quota=30))
        event.add_ticket_category(make_category(quota=20))
        event.publish()
        event.cancel()
        assert all(not c.is_active for c in event.ticket_categories)

    def test_records_event_cancelled_domain_event(self):
        """US:3 — AC: sistem memunculkan domain event EventCancelled."""
        from src.domain.events.event_cancelled import EventCancelled
        event = make_event()
        event.add_ticket_category(make_category())
        event.publish()
        event.cancel()
        types = [type(e) for e in event.domain_events]
        assert EventCancelled in types


# ─────────────────────────────────────────
# US:4 — CREATE TICKET CATEGORY
# ─────────────────────────────────────────

class TestAddTicketCategory:

    def test_add_ticket_category_successfully(self):
        """US:4 — AC: ticket category berhasil ditambahkan ke event."""
        event = make_event(capacity=100)
        category = make_category(quota=50)
        event.add_ticket_category(category)
        assert len(event.ticket_categories) == 1

    def test_raises_if_quota_exceeds_capacity(self):
        """US:4 — AC: total quota tidak boleh melebihi capacity event."""
        event = make_event(capacity=100)
        event.add_ticket_category(make_category(quota=70))
        with pytest.raises(ValueError):
            event.add_ticket_category(make_category(quota=40))  # 70+40=110 > 100

    def test_raises_if_quota_is_zero(self):
        """US:4 — AC: quota harus > 0."""
        with pytest.raises(ValueError):
            make_category(quota=0)

    def test_raises_if_quota_is_negative(self):
        """US:4 — AC: quota harus > 0."""
        with pytest.raises(ValueError):
            make_category(quota=-5)

    def test_raises_if_price_is_negative(self):
        """US:4 — AC: harga ticket tidak boleh negatif."""
        with pytest.raises(ValueError):
            make_category(price=Decimal("-1000"))

    def test_raises_if_sales_end_after_event_start(self):
        """US:4 — AC: sales period harus berakhir sebelum atau saat event mulai."""
        event = make_event()   # event start: 2025-02-10
        category = make_category(
            sales_start=datetime(2025, 1, 1),
            sales_end=datetime(2025, 2, 15),   # setelah event start — tidak valid
        )
        with pytest.raises(ValueError):
            event.add_ticket_category(category)

    def test_sales_end_on_event_start_is_allowed(self):
        """US:4 — AC: sales end boleh sama dengan event start date."""
        event = make_event()   # event start: 2025-02-10
        category = make_category(
            sales_start=datetime(2025, 1, 1),
            sales_end=datetime(2025, 2, 10),   # tepat saat event mulai — valid
        )
        event.add_ticket_category(category)
        assert len(event.ticket_categories) == 1

    def test_multiple_categories_within_capacity(self):
        """US:4 — AC: beberapa kategori bisa ditambah selama total quota <= capacity."""
        event = make_event(capacity=100)
        event.add_ticket_category(make_category(quota=30))
        event.add_ticket_category(make_category(quota=30))
        event.add_ticket_category(make_category(quota=40))
        assert len(event.ticket_categories) == 3

    def test_records_ticket_category_created_domain_event(self):
        """US:4 — AC: sistem memunculkan domain event TicketCategoryCreated."""
        from src.domain.events.ticket_category_created import TicketCategoryCreated
        event = make_event()
        event.add_ticket_category(make_category())
        types = [type(e) for e in event.domain_events]
        assert TicketCategoryCreated in types


# ─────────────────────────────────────────
# US:5 — DISABLE TICKET CATEGORY
# ─────────────────────────────────────────

class TestDisableTicketCategory:

    def test_disable_ticket_category_successfully(self):
        """US:5 — AC: ticket category bisa di-disable."""
        category = make_category()
        category.disable()
        assert category.is_active is False

    def test_disabled_category_not_counted_as_active(self):
        """US:5 — AC: kategori non-aktif tidak dianggap tersedia untuk pembelian."""
        event = make_event()
        category = make_category()
        event.add_ticket_category(category)
        category.disable()
        active = [c for c in event.ticket_categories if c.is_active]
        assert len(active) == 0

    def test_disabled_category_still_stored(self):
        """US:5 — AC: kategori yang di-disable tetap disimpan untuk histori."""
        event = make_event()
        category = make_category()
        event.add_ticket_category(category)
        category.disable()
        assert category in event.ticket_categories  # masih ada di list

    def test_cannot_publish_after_only_category_disabled(self):
        """US:5 + US:2 — publish gagal jika semua kategori di-disable."""
        event = make_event()
        category = make_category()
        event.add_ticket_category(category)
        category.disable()
        with pytest.raises(ValueError):
            event.publish()

    def test_records_ticket_category_disabled_domain_event_on_cancel(self):
        """US:5 — AC: EventCancelled memicu TicketCategoryDisabled untuk tiap kategori."""
        from src.domain.events.ticket_category_disabled import TicketCategoryDisabled
        event = make_event()
        event.add_ticket_category(make_category(quota=30))
        event.add_ticket_category(make_category(quota=20))
        event.publish()
        event.cancel()
        disabled_events = [e for e in event.domain_events if isinstance(e, TicketCategoryDisabled)]
        assert len(disabled_events) == 2