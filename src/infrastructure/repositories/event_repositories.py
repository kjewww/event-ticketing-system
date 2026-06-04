from uuid import UUID
from src.domain.aggregates.event import Event
from src.domain.repositories.event_repository import EventRepository


class SqlAlchemyEventRepository(EventRepository):
    def __init__(self, session):
        self.session = session

    def get_by_id(self, event_id: UUID) -> Event | None:
        return self.session.query(Event).filter_by(id=event_id).first()

    def save(self, event: Event) -> None:
        self.session.add(event)
        self.session.commit()