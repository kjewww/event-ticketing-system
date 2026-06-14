from datetime import date as Date
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from src.application.dto.event_dto import AvailableEventDTO, EventDetailsDTO
from src.application.dto.ticket_category_dto import TicketCategoryDTO
from src.application.interfaces.event_read_repository import EventReadRepository
from src.domain.value_objects.booking_status import BookingStatus
from src.domain.value_objects.event_status import EventStatus
from src.infrastructure.database.models.booking_model import BookingModel
from src.infrastructure.database.models.event_model import EventModel
from src.infrastructure.database.models.ticket_category_model import TicketCategoryModel


class SqlAlchemyEventReadRepository(EventReadRepository):
    def __init__(self, session: Session):
        self.session = session

    def find_available_events(
        self,
        date: Date | datetime | None = None,
        location: str | None = None,
    ) -> list[AvailableEventDTO]:
        lowest_price = func.min(TicketCategoryModel.price_amount).label(
            "lowest_ticket_price"
        )

        query = (
            self.session.query(
                EventModel.id,
                EventModel.name,
                EventModel.start_date,
                EventModel.end_date,
                EventModel.location,
                lowest_price,
            )
            .join(
                TicketCategoryModel,
                TicketCategoryModel.event_id == EventModel.id,
            )
            .filter(EventModel.status == EventStatus.PUBLISHED.value)
            .filter(TicketCategoryModel.is_active.is_(True))
            .group_by(
                EventModel.id,
                EventModel.name,
                EventModel.start_date,
                EventModel.end_date,
                EventModel.location,
            )
            .order_by(EventModel.start_date.asc())
        )

        if date is not None:
            date_filter = date.date() if isinstance(date, datetime) else date
            query = query.filter(EventModel.start_date <= date_filter)
            query = query.filter(EventModel.end_date >= date_filter)

        if location:
            query = query.filter(EventModel.location.ilike(f"%{location}%"))

        rows = query.all()

        return [
            AvailableEventDTO(
                event_id=row.id,
                name=row.name,
                start_date=row.start_date,
                end_date=row.end_date,
                location=row.location,
                lowest_ticket_price=row.lowest_ticket_price or Decimal("0"),
            )
            for row in rows
        ]

    def get_event_details(self, event_id: UUID) -> EventDetailsDTO | None:
        event = (
            self.session.query(EventModel)
            .options(joinedload(EventModel.ticket_categories))
            .filter(EventModel.id == event_id)
            .filter(EventModel.status == EventStatus.PUBLISHED.value)
            .first()
        )

        if event is None:
            return None

        ticket_categories = []

        for category in event.ticket_categories:
            if not category.is_active:
                continue

            remaining_quota = self._calculate_remaining_quota(category)
            purchase_status = self._determine_purchase_status(
                category=category,
                remaining_quota=remaining_quota,
            )

            ticket_categories.append(
                TicketCategoryDTO(
                    ticket_category_id=category.id,
                    name=category.name,
                    price_amount=category.price_amount,
                    currency=category.price_currency,
                    quota=category.quota,
                    remaining_quota=remaining_quota,
                    sales_start_date=category.sales_start_date,
                    sales_end_date=category.sales_end_date,
                    is_active=category.is_active,
                    purchase_status=purchase_status,
                )
            )

        return EventDetailsDTO(
            event_id=event.id,
            name=event.name,
            description=event.description,
            start_date=event.start_date,
            end_date=event.end_date,
            location=event.location,
            organizer_id=event.organizer_id,
            status=event.status,
            ticket_categories=ticket_categories,
        )

    def _calculate_remaining_quota(
        self,
        category: TicketCategoryModel,
    ) -> int:
        reserved_or_sold_statuses = [
            BookingStatus.PENDING_PAYMENT.value,
            BookingStatus.PAID.value,
        ]

        used_quantity = (
            self.session.query(func.coalesce(func.sum(BookingModel.quantity), 0))
            .filter(BookingModel.ticket_category_id == category.id)
            .filter(BookingModel.status.in_(reserved_or_sold_statuses))
            .scalar()
        )

        return max(category.quota - int(used_quantity), 0)

    def _determine_purchase_status(
        self,
        category: TicketCategoryModel,
        remaining_quota: int,
    ) -> str:
        today = Date.today()

        if today < category.sales_start_date:
            return "Coming Soon"

        if today > category.sales_end_date:
            return "Sales Closed"

        if remaining_quota <= 0:
            return "Sold Out"

        return "Available"