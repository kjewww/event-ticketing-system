from src.application.dto.report_dto import EventParticipantDTO
from src.application.interfaces.report_read_repository import ReportReadRepository
from src.application.queries.view_event_participants_query import (
    ViewEventParticipantsQuery,
)

from src.domain.repositories.event_repository import EventRepository


class ViewEventParticipantsQueryHandler:
    def __init__(
        self,
        event_repository: EventRepository,
        report_read_repository: ReportReadRepository,
    ):
        self.event_repository = event_repository
        self.report_read_repository = report_read_repository

    def handle(
        self,
        query: ViewEventParticipantsQuery,
    ) -> list[EventParticipantDTO]:
        event = self.event_repository.get_by_id(query.event_id)

        if event is None:
            raise ValueError("Event not found.")

        if str(event.organizer_id) != str(query.organizer_id):
            raise PermissionError("Only the event organizer can view participants.")

        return self.report_read_repository.get_event_participants(
            event_id=query.event_id,
        )