from uuid import UUID

from sqlalchemy.orm import Session, joinedload

from src.domain.aggregates.event import Event
from src.domain.repositories.event_repository import EventRepository

from src.infrastructure.database.models.event_model import EventModel
from src.infrastructure.mappers.event_mapper import EventMapper


class SqlAlchemyEventRepository(EventRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, event_id: UUID) -> Event | None:
        model = (
            self.session.query(EventModel)
            .options(joinedload(EventModel.ticket_categories))
            .filter(EventModel.id == event_id)
            .first()
        )

        if model is None:
            return None

        return EventMapper.to_domain(model)

    def save(self, event: Event) -> None:
        model = EventMapper.to_model(event)
        self.session.merge(model)