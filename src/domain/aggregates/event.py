from datetime import datetime
from uuid import uuid4, UUID

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
    TicketCategoryCannotBeDisabledError
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
        self.domain_events = []
        self.domain_events.append(EventCreated(self.id))


    def add_ticket_category(self, category: TicketCategory):
            current_total_quota: int = 0
            for c in self.ticket_categories:
                current_total_quota += c.quota
                
            if current_total_quota + category.quota > self.capacity:
                raise EventTicketCategoryQuotaExceededError(f"Total quota ({current_total_quota + category.quota}) exceeds event capacity ({self.capacity})")
            
            if category.sales_date_range.end_date > self.date_range.start_date:
                raise ValueError("Ticket sales period must end before event starts.")
            
            self.ticket_categories.append(category)
            self.domain_events.append(TicketCategoryCreated(category.id))

    def publish(self):
        if self.status != EventStatus.DRAFT:
            raise ValueError("only draft event can be published")
        
        active_categories = []
        for c in self.ticket_categories:
            if c.is_active:
                active_categories.append(c)
        
        if not active_categories:
            raise EventCannotBePublishedError("Event must have at least one active ticket category.")
        
        self.status = EventStatus.PUBLISHED
        self.domain_events.append(EventPublished(self.id))

    def cancel(self):
        if self.status != EventStatus.PUBLISHED:
            raise EventCannotBeCancelledError("Only published events can be cancelled")
        
        for c in self.ticket_categories:
            c.disable()
            self.domain_events.append(TicketCategoryDisabled(c.id))
        
        self.status = EventStatus.CANCELLED
        self.domain_events.append(EventCancelled(self.id))

    def disable_ticket_category(self, ticketCategory: TicketCategory):
        if self.status == EventStatus.COMPLETED:
            raise TicketCategoryCannotBeDisabledError("Ticket category cant be disabled on completed event")
        
        ticketCategory.disable()
        self.domain_events.append(TicketCategoryDisabled(ticketCategory.id))
        
        
        