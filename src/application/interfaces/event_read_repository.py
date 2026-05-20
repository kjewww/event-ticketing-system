from abc import ABC, abstractmethod


class EventReadRepository(ABC):
    @abstractmethod
    def find_available_events(self, date=None, location=None):
        pass

    @abstractmethod
    def get_event_details(self, event_id):
        pass