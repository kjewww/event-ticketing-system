from src.domain.entities.ticket import Ticket
from src.domain.value_objects.ticket_code import TicketCode
from src.domain.value_objects.ticket_status import TicketStatus

from src.infrastructure.database.models.ticket_model import TicketModel


class TicketMapper:
    @staticmethod
    def to_domain(model: TicketModel) -> Ticket:
        return Ticket(
            id=model.id,
            booking_id=model.booking_id,
            event_id=model.event_id,
            ticket_category_id=model.ticket_category_id,
            ticket_code=TicketCode(model.ticket_code),
            status=TicketStatus(model.status),
            checked_in_at=model.checked_in_at,
        )

    @staticmethod
    def to_model(domain: Ticket) -> TicketModel:
        return TicketModel(
            id=domain.id,
            booking_id=domain.booking_id,
            event_id=domain.event_id,
            ticket_category_id=domain.ticket_category_id,
            ticket_code=domain.ticket_code.value,
            status=domain.status.value,
            checked_in_at=domain.checked_in_at,
        )