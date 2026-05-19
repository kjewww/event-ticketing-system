from datetime import date
from decimal import Decimal

import pytest

from src.domain.entities.ticket_category import TicketCategory
from src.domain.exceptions.domain_exception import (
    InvalidTicketCategoryNameError,
    InvalidTicketCategoryQuotaError,
)
from src.domain.value_objects.date_range import DateRange
from src.domain.value_objects.money import Money


def test_ticket_category_requires_name():
    with pytest.raises(InvalidTicketCategoryNameError):
        TicketCategory(
            name="   ",
            price=Money(Decimal("0")),
            quota=10,
            sales_date_range=DateRange(date(2026, 6, 1), date(2026, 7, 1)),
        )


def test_ticket_category_quota_must_be_greater_than_zero():
    with pytest.raises(InvalidTicketCategoryQuotaError):
        TicketCategory(
            name="Regular",
            price=Money(Decimal("0")),
            quota=0,
            sales_date_range=DateRange(date(2026, 6, 1), date(2026, 7, 1)),
        )


def test_ticket_category_can_be_disabled():
    category = TicketCategory(
        name="Regular",
        price=Money(Decimal("0")),
        quota=10,
        sales_date_range=DateRange(date(2026, 6, 1), date(2026, 7, 1)),
    )

    category.disable()

    assert category.is_active is False
