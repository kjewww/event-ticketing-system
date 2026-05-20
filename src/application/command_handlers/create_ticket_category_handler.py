from decimal import Decimal

from src.application.commands.create_ticket_category_command import (
    CreateTicketCategoryCommand,
)
from src.application.dto.ticket_category_dto import (
    CreateTicketCategoryResponseDTO,
)
from src.application.interfaces.unit_of_work import UnitOfWork

from src.domain.entities.ticket_category import TicketCategory
from src.domain.repositories.event_repository import EventRepository
from src.domain.value_objects.date_range import DateRange
from src.domain.value_objects.money import Money


class CreateTicketCategoryCommandHandler:
    def __init__(
        self,
        event_repository: EventRepository,
        unit_of_work: UnitOfWork,
    ):
        self.event_repository = event_repository
        self.unit_of_work = unit_of_work

    def handle(
        self,
        command: CreateTicketCategoryCommand,
    ) -> CreateTicketCategoryResponseDTO:
        try:
            event = self.event_repository.get_by_id(command.event_id)

            if event is None:
                raise ValueError("Event not found.")

            if event.organizer_id != command.organizer_id:
                raise PermissionError(
                    "Only the event organizer can manage ticket categories."
                )

            price = Money(
                amount=Decimal(str(command.price_amount)),
                currency=command.currency,
            )

            sales_date_range = DateRange(
                start_date=command.sales_start_date,
                end_date=command.sales_end_date,
            )

            ticket_category = TicketCategory(
                name=command.name,
                price=price,
                quota=command.quota,
                sales_date_range=sales_date_range,
            )

            event.add_ticket_category(ticket_category)

            self.event_repository.save(event)
            self.unit_of_work.commit()

            return CreateTicketCategoryResponseDTO(
                event_id=event.id,
                ticket_category_id=ticket_category.id,
                name=ticket_category.name,
                price_amount=ticket_category.price.amount,
                currency=ticket_category.price.currency,
                quota=ticket_category.quota,
                sales_start_date=ticket_category.sales_date_range.start_date,
                sales_end_date=ticket_category.sales_date_range.end_date,
                is_active=ticket_category.is_active,
            )

        except Exception:
            self.unit_of_work.rollback()
            raise