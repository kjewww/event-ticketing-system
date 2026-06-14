from uuid import UUID

from sqlalchemy.orm import Session

from src.application.dto.ticket_dto import PurchasedTicketDTO
from src.application.interfaces.booking_read_repository import BookingReadRepository
from src.domain.value_objects.booking_status import BookingStatus
from src.infrastructure.database.models.booking_model import BookingModel
from src.infrastructure.database.models.event_model import EventModel
from src.infrastructure.database.models.ticket_category_model import TicketCategoryModel
from src.infrastructure.database.models.ticket_model import TicketModel


class SqlAlchemyBookingReadRepository(BookingReadRepository):
    def __init__(self, session: Session):
        self.session = session

    def find_purchased_tickets_by_customer(
        self,
        customer_id: UUID,
    ) -> list[PurchasedTicketDTO]:
        rows = (
            self.session.query(
                TicketModel.id.label("ticket_id"),
                BookingModel.id.label("booking_id"),
                EventModel.id.label("event_id"),
                EventModel.name.label("event_name"),
                TicketCategoryModel.id.label("ticket_category_id"),
                TicketCategoryModel.name.label("ticket_category_name"),
                TicketModel.ticket_code,
                TicketModel.status,
                TicketModel.checked_in_at,
            )
            .join(BookingModel, BookingModel.id == TicketModel.booking_id)
            .join(EventModel, EventModel.id == BookingModel.event_id)
            .join(
                TicketCategoryModel,
                TicketCategoryModel.id == TicketModel.ticket_category_id,
            )
            .filter(BookingModel.customer_id == customer_id)
            .filter(BookingModel.status == BookingStatus.PAID.value)
            .order_by(EventModel.start_date.asc(), TicketModel.ticket_code.asc())
            .all()
        )

        return [
            PurchasedTicketDTO(
                ticket_id=row.ticket_id,
                booking_id=row.booking_id,
                event_id=row.event_id,
                event_name=row.event_name,
                ticket_category_id=row.ticket_category_id,
                ticket_category_name=row.ticket_category_name,
                ticket_code=row.ticket_code,
                status=row.status,
                checked_in_at=row.checked_in_at,
            )
            for row in rows
        ]