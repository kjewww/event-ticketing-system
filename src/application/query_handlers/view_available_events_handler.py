from src.application.dto.event_dto import AvailableEventDTO
from src.application.interfaces.event_read_repository import EventReadRepository
from src.application.queries.view_available_events_query import (
    ViewAvailableEventsQuery,
)


class ViewAvailableEventsQueryHandler:
    def __init__(self, event_read_repository: EventReadRepository):
        self.event_read_repository = event_read_repository

    def handle(self, query: ViewAvailableEventsQuery) -> list[AvailableEventDTO]:
        return self.event_read_repository.find_available_events(
            date_filter=query.date_filter,
            location=query.location,
        )