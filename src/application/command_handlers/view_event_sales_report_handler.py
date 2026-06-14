from src.application.dto.report_dto import EventSalesReportDTO
from src.application.interfaces.report_read_repository import ReportReadRepository
from src.application.queries.view_event_sales_report_query import (
    ViewEventSalesReportQuery,
)

from src.domain.repositories.event_repository import EventRepository


class ViewEventSalesReportQueryHandler:
    def __init__(
        self,
        event_repository: EventRepository,
        report_read_repository: ReportReadRepository,
    ):
        self.event_repository = event_repository
        self.report_read_repository = report_read_repository

    def handle(
        self,
        query: ViewEventSalesReportQuery,
    ) -> EventSalesReportDTO:
        event = self.event_repository.get_by_id(query.event_id)

        if event is None:
            raise ValueError("Event not found.")

        if str(event.organizer_id) != str(query.organizer_id):
            raise PermissionError("Only the event organizer can view this sales report.")

        return self.report_read_repository.get_event_sales_report(
            event_id=query.event_id,
        )