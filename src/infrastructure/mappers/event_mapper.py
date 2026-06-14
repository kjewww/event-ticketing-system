from src.domain.aggregates.event import Event
from src.domain.value_objects.date_range import DateRange
from src.domain.value_objects.event_status import EventStatus

from src.infrastructure.database.models.event_model import EventModel
from src.infrastructure.mappers.ticket_category_mapper import TicketCategoryMapper


class EventMapper:
    @staticmethod
    def to_domain(model: EventModel) -> Event:
        ticket_categories = [
            TicketCategoryMapper.to_domain(category_model)
            for category_model in model.ticket_categories
        ]

        return Event.reconstruct(
            id=model.id,
            organizer_id=model.organizer_id,
            name=model.name,
            description=model.description,
            date_range=DateRange(
                model.start_date,
                model.end_date,
            ),
            location=model.location,
            capacity=model.capacity,
            status=EventStatus(model.status),
            ticket_categories=ticket_categories,
        )

    @staticmethod
    def to_model(domain: Event) -> EventModel:
        model = EventModel(
            id=domain.id,
            organizer_id=domain.organizer_id,
            name=domain.name,
            description=domain.description,
            location=domain.location,
            start_date=domain.date_range.start_date,
            end_date=domain.date_range.end_date,
            capacity=domain.capacity,
            status=domain.status.value,
        )

        model.ticket_categories = [
            TicketCategoryMapper.to_model(
                category,
                event_id=domain.id,
            )
            for category in domain.ticket_categories
        ]

        return model