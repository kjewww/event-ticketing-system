from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.aggregates.event import Event


class EventRepository(ABC):
    @abstractmethod
    def get_by_id(self, event_id: UUID) -> Event | None:
        pass

    @abstractmethod
    def save(self, event: Event) -> None:
        pass