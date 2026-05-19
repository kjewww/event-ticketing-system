from uuid import uuid4

from src.domain.exceptions.domain_exception import (
    InvalidTicketCategoryNameError,
    InvalidTicketCategoryQuotaError,
)
from src.domain.value_objects.date_range import DateRange
from src.domain.value_objects.money import Money


class TicketCategory:
    def __init__(
        self,
        name: str,
        price: Money,
        quota: int,
        sales_date_range: DateRange,
    ):
        if not name or not name.strip():
            raise InvalidTicketCategoryNameError(
                "Ticket category name is required."
            )

        if quota <= 0:
            raise InvalidTicketCategoryQuotaError(
                "Quota must be greater than zero."
            )

        self.id = uuid4()
        self.name = name
        self.price = price
        self.quota = quota
        self.sales_date_range = sales_date_range
        self.is_active: bool = True

    def disable(self) -> None:
        self.is_active = False