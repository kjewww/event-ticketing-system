from abc import ABC, abstractmethod
from datetime import date, datetime
from uuid import UUID

from src.application.dto.event_dto import AvailableEventDTO, EventDetailsDTO


class EventReadRepository(ABC):
    @abstractmethod
    def find_available_events(
        self,
        date_filter: date | datetime | None = None,
        location: str | None = None,
    ) -> list[AvailableEventDTO]:
        pass

    @abstractmethod
    def get_event_details(
        self,
        event_id: UUID,
    ) -> EventDetailsDTO | None:
        pass