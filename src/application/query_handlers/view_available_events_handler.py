from src.application.dto.event_dto import AvailableEventDTO
from src.application.interfaces.event_read_repository import EventReadRepository
from src.application.queries.view_available_events_query import (
    ViewAvailableEventsQuery,
)


class ViewAvailableEventsQueryHandler:
    def __init__(self, event_read_repository: EventReadRepository):
        self.event_read_repository = event_read_repository

    def handle(self, query: ViewAvailableEventsQuery) -> list[AvailableEventDTO]:
        events = self.event_read_repository.find_available_events(
            date=query.date_filter,
            location=query.location,
        )

        return [
            AvailableEventDTO(
                event_id=event.event_id,
                name=event.name,
                start_date=event.start_date,
                end_date=event.end_date,
                location=event.location,
                lowest_ticket_price=event.lowest_ticket_price,
            )
            for event in events
        ]