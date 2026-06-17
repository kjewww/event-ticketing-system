from decimal import Decimal
from uuid import UUID

from sqlalchemy import case, func
from sqlalchemy.orm import Session

from src.application.dto.report_dto import (
    BookingStatusCountDTO,
    EventParticipantDTO,
    EventSalesReportDTO,
    TicketCategorySalesDTO,
)
from src.application.interfaces.report_read_repository import ReportReadRepository
from src.domain.value_objects.booking_status import BookingStatus
from src.infrastructure.database.models.booking_model import BookingModel
from src.infrastructure.database.models.ticket_category_model import TicketCategoryModel
from src.infrastructure.database.models.ticket_model import TicketModel


class SqlAlchemyReportReadRepository(ReportReadRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_event_sales_report(
        self,
        event_id: UUID,
    ) -> EventSalesReportDTO:
        tickets_sold_per_category = self._get_tickets_sold_per_category(event_id)
        booking_status_counts = self._get_booking_status_counts(event_id)
        total_revenue_amount, currency = self._get_total_revenue(event_id)

        return EventSalesReportDTO(
            event_id=event_id,
            tickets_sold_per_category=tickets_sold_per_category,
            booking_status_counts=booking_status_counts,
            total_revenue_amount=total_revenue_amount,
            currency=currency,
        )

    def get_event_participants(
        self,
        event_id: UUID,
    ) -> list[EventParticipantDTO]:
        rows = (
            self.session.query(
                BookingModel.customer_id,
                BookingModel.customer_name,
                TicketCategoryModel.name.label("ticket_category_name"),
                TicketModel.ticket_code,
                TicketModel.status.label("check_in_status"),
            )
            .join(TicketModel, TicketModel.booking_id == BookingModel.id)
            .join(
                TicketCategoryModel,
                TicketCategoryModel.id == TicketModel.ticket_category_id,
            )
            .filter(BookingModel.event_id == event_id)
            .filter(BookingModel.status == BookingStatus.PAID.value)
            .order_by(BookingModel.customer_name.asc(), TicketModel.ticket_code.asc())
            .all()
        )

        return [
            EventParticipantDTO(
                customer_id=row.customer_id,
                customer_name=row.customer_name,
                ticket_category_name=row.ticket_category_name,
                ticket_code=row.ticket_code,
                check_in_status=row.check_in_status,
            )
            for row in rows
        ]

    def _get_tickets_sold_per_category(
        self,
        event_id: UUID,
    ) -> list[TicketCategorySalesDTO]:
        paid_ticket_count = func.coalesce(
            func.sum(
                case(
                    (BookingModel.status == BookingStatus.PAID.value, 1),
                    else_=0,
                )
            ),
            0,
        ).label("tickets_sold")

        rows = (
            self.session.query(
                TicketCategoryModel.id.label("ticket_category_id"),
                TicketCategoryModel.name.label("ticket_category_name"),
                paid_ticket_count,
            )
            .outerjoin(
                TicketModel,
                TicketModel.ticket_category_id == TicketCategoryModel.id,
            )
            .outerjoin(
                BookingModel,
                BookingModel.id == TicketModel.booking_id,
            )
            .filter(TicketCategoryModel.event_id == event_id)
            .group_by(TicketCategoryModel.id, TicketCategoryModel.name)
            .order_by(TicketCategoryModel.name.asc())
            .all()
        )

        return [
            TicketCategorySalesDTO(
                ticket_category_id=row.ticket_category_id,
                ticket_category_name=row.ticket_category_name,
                tickets_sold=int(row.tickets_sold),
            )
            for row in rows
        ]

    def _get_booking_status_counts(
        self,
        event_id: UUID,
    ) -> list[BookingStatusCountDTO]:
        expected_statuses = [
            BookingStatus.PENDING_PAYMENT.value,
            BookingStatus.PAID.value,
            BookingStatus.EXPIRED.value,
            BookingStatus.REFUNDED.value,
        ]

        status_counts = {
            status: 0
            for status in expected_statuses
        }

        rows = (
            self.session.query(
                BookingModel.status,
                func.count(BookingModel.id).label("count"),
            )
            .filter(BookingModel.event_id == event_id)
            .filter(BookingModel.status.in_(expected_statuses))
            .group_by(BookingModel.status)
            .all()
        )

        for row in rows:
            status_counts[row.status] = int(row.count)

        return [
            BookingStatusCountDTO(
                status=status,
                count=count,
            )
            for status, count in status_counts.items()
        ]

    def _get_total_revenue(
        self,
        event_id: UUID,
    ) -> tuple[Decimal, str]:
        row = (
            self.session.query(
                func.coalesce(
                    func.sum(BookingModel.total_price_amount),
                    Decimal("0"),
                ).label("total_revenue_amount"),
                func.max(BookingModel.total_price_currency).label("currency"),
            )
            .filter(BookingModel.event_id == event_id)
            .filter(BookingModel.status == BookingStatus.PAID.value)
            .first()
        )

        return (
            row.total_revenue_amount or Decimal("0"),
            row.currency or "IDR",
        )