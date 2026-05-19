from uuid import UUID, uuid4

from src.domain.value_objects.date_range import DateRange
from src.domain.value_objects.event_status import EventStatus
from src.domain.entities.ticket_category import TicketCategory

from src.domain.events.event_events import (
    EventCreated, 
    EventCancelled, 
    EventPublished
)
from src.domain.events.ticket_category_events import (
    TicketCategoryCreated, 
    TicketCategoryDisabled
)
from src.domain.exceptions.domain_exception import (
    InvalidEventCapacityError, 
    EventCannotBePublishedError, 
    EventCannotBeCancelledError, 
    EventTicketCategoryQuotaExceededError, 
    EventTicketCategoryNotAllowedError,
)

class Event:
    def __init__(
        self, 
        organizer_id: UUID,
        name: str, 
        description: str, 
        date_range: DateRange,
        location: str,
        capacity: int
    ):

        if capacity <= 0:
            raise InvalidEventCapacityError("Capacity must be greater than zero!")
        
        self.organizer_id = organizer_id
        self.id = uuid4()
        self.name = name
        self.description = description
        self.date_range = date_range
        self.location = location
        self.capacity = capacity
        self.status = EventStatus.DRAFT
        self.ticket_categories: list[TicketCategory] = []
        self.domain_events = [EventCreated(self.id)]

    def add_ticket_category(self, category: TicketCategory) -> None:
        current_total_quota = sum(
            category.quota for category in self.ticket_categories
        )

        new_total_quota = current_total_quota + category.quota

        if new_total_quota > self.capacity:
            raise EventTicketCategoryQuotaExceededError(
                f"Total quota ({new_total_quota}) exceeds event capacity ({self.capacity})."
            )

        if category.sales_date_range.end_date > self.date_range.start_date:
            raise EventTicketCategoryNotAllowedError(
                "Ticket sales period must end before or at the event start date."
            )

        self.ticket_categories.append(category)

        self.domain_events.append(
            TicketCategoryCreated(
                event_id=self.id,
                ticket_category_id=category.id,
            )
        )

    def publish(self) -> None:
        if self.status != EventStatus.DRAFT:
            raise EventCannotBePublishedError(
                "Only draft event can be published."
            )

        active_categories = [
            category
            for category in self.ticket_categories
            if category.is_active
        ]

        if not active_categories:
            raise EventCannotBePublishedError(
                "Event must have at least one active ticket category."
            )

        self.status = EventStatus.PUBLISHED
        self.domain_events.append(EventPublished(self.id))

    def cancel(self) -> None:
        if self.status != EventStatus.PUBLISHED:
            raise EventCannotBeCancelledError(
                "Only published events can be cancelled."
            )

        for category in self.ticket_categories:
            if category.is_active:
                category.disable()
                self.domain_events.append(
                    TicketCategoryDisabled(
                        event_id=self.id,
                        ticket_category_id=category.id,
                    )
                )

        self.status = EventStatus.CANCELLED
        self.domain_events.append(EventCancelled(self.id))

    def disable_ticket_category(self, ticket_category_id: UUID) -> None:
        if self.status == EventStatus.COMPLETED:
            raise EventTicketCategoryNotAllowedError(
                "Ticket category cannot be disabled on completed event."
            )

        category = next(
            (
                category
                for category in self.ticket_categories
                if category.id == ticket_category_id
            ),
            None,
        )

        if category is None:
            raise EventTicketCategoryNotAllowedError(
                "Ticket category does not belong to this event."
            )

        if category.is_active:
            category.disable()

            self.domain_events.append(
                TicketCategoryDisabled(
                    event_id=self.id,
                    ticket_category_id=category.id,
                )
            )