from uuid import UUID, uuid4

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
        id: UUID | None = None,
        is_active: bool = True,
    ):
        if not name or not name.strip():
            raise InvalidTicketCategoryNameError(
                "Ticket category name is required."
            )

        if quota <= 0:
            raise InvalidTicketCategoryQuotaError(
                "Quota must be greater than zero."
            )

        self.id = id or uuid4()
        self.name = name
        self.price = price
        self.quota = quota
        self.sales_date_range = sales_date_range
        self.is_active = is_active

    @classmethod
    def create(
        cls,
        name: str,
        price: Money,
        quota: int,
        sales_date_range: DateRange,
    ) -> "TicketCategory":
        return cls(
            name=name,
            price=price,
            quota=quota,
            sales_date_range=sales_date_range,
            is_active=True,
        )

    @classmethod
    def reconstruct(
        cls,
        id: UUID,
        name: str,
        price: Money,
        quota: int,
        sales_date_range: DateRange,
        is_active: bool,
    ) -> "TicketCategory":
        return cls(
            id=id,
            name=name,
            price=price,
            quota=quota,
            sales_date_range=sales_date_range,
            is_active=is_active,
        )

    def disable(self) -> None:
        self.is_active = False