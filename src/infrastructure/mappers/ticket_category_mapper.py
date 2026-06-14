from src.domain.entities.ticket_category import TicketCategory
from src.domain.value_objects.date_range import DateRange
from src.domain.value_objects.money import Money

from src.infrastructure.database.models.ticket_category_model import TicketCategoryModel


class TicketCategoryMapper:
    @staticmethod
    def to_domain(model: TicketCategoryModel) -> TicketCategory:
        return TicketCategory.reconstruct(
            id=model.id,
            name=model.name,
            price=Money(
                amount=model.price_amount,
                currency=model.price_currency,
            ),
            quota=model.quota,
            sales_date_range=DateRange(
                model.sales_start_date,
                model.sales_end_date,
            ),
            is_active=model.is_active,
        )

    @staticmethod
    def to_model(
        domain: TicketCategory,
        event_id,
    ) -> TicketCategoryModel:
        return TicketCategoryModel(
            id=domain.id,
            event_id=event_id,
            name=domain.name,
            price_amount=domain.price.amount,
            price_currency=domain.price.currency,
            quota=domain.quota,
            sales_start_date=domain.sales_date_range.start_date,
            sales_end_date=domain.sales_date_range.end_date,
            is_active=domain.is_active,
        )