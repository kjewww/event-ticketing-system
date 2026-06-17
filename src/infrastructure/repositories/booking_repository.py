from uuid import UUID

from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from src.domain.aggregates.booking import Booking
from src.domain.repositories.booking_repository import BookingRepository
from src.domain.value_objects.booking_status import BookingStatus
from src.domain.value_objects.ticket_code import TicketCode

from src.infrastructure.database.models.booking_model import BookingModel
from src.infrastructure.database.models.ticket_model import TicketModel
from src.infrastructure.mappers.booking_mapper import BookingMapper


class SqlAlchemyBookingRepository(BookingRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, booking_id: UUID) -> Booking | None:
        model = (
            self.session.query(BookingModel)
            .options(joinedload(BookingModel.tickets))
            .filter(BookingModel.id == booking_id)
            .first()
        )

        if model is None:
            return None

        return BookingMapper.to_domain(model)

    def get_by_ticket_code(self, ticket_code: TicketCode) -> Booking | None:
        model = (
            self.session.query(BookingModel)
            .join(TicketModel, TicketModel.booking_id == BookingModel.id)
            .options(joinedload(BookingModel.tickets))
            .filter(TicketModel.ticket_code == ticket_code.value)
            .first()
        )

        if model is None:
            return None

        return BookingMapper.to_domain(model)

    def save(self, booking: Booking) -> None:
        model = BookingMapper.to_model(booking)
        self.session.merge(model)

    def has_active_booking_for_event(
        self,
        customer_id: UUID,
        event_id: UUID,
    ) -> bool:
        active_statuses = [
            BookingStatus.PENDING_PAYMENT.value,
            BookingStatus.PAID.value,
        ]

        count = (
            self.session.query(func.count(BookingModel.id))
            .filter(BookingModel.customer_id == customer_id)
            .filter(BookingModel.event_id == event_id)
            .filter(BookingModel.status.in_(active_statuses))
            .scalar()
        )

        return count > 0

    def get_paid_bookings_by_event_id(
        self,
        event_id: UUID,
    ) -> list[Booking]:
        models = (
            self.session.query(BookingModel)
            .options(joinedload(BookingModel.tickets))
            .filter(BookingModel.event_id == event_id)
            .filter(BookingModel.status == BookingStatus.PAID.value)
            .all()
        )

        return [
            BookingMapper.to_domain(model)
            for model in models
        ]

    def get_by_customer_id(
        self,
        customer_id: UUID,
    ) -> list[Booking]:
        models = (
            self.session.query(BookingModel)
            .options(joinedload(BookingModel.tickets))
            .filter(BookingModel.customer_id == customer_id)
            .all()
        )

        return [
            BookingMapper.to_domain(model)
            for model in models
        ]

    def count_reserved_or_sold_quantity(
        self,
        ticket_category_id: UUID,
    ) -> int:
        active_statuses = [
            BookingStatus.PENDING_PAYMENT.value,
            BookingStatus.PAID.value,
        ]

        total = (
            self.session.query(func.coalesce(func.sum(BookingModel.quantity), 0))
            .filter(BookingModel.ticket_category_id == ticket_category_id)
            .filter(BookingModel.status.in_(active_statuses))
            .scalar()
        )

        return int(total)