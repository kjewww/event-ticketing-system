from uuid import uuid4

from src.domain.value_objects.date_range import DateRange
from src.domain.value_objects.event_status import EventStatus

from src.domain.events.event_created import EventCreated
from src.domain.events.event_published import EventPublished
from src.domain.events.event_cancelled import EventCancelled

from src.domain.entities.ticket_category import TicketCategory

class Event:
    def __init__(
        self, 
        name: str, 
        description: str, 
        date_range: DateRange,
        location: str,
        capacity: int
        ):
        
        if capacity <= 0:
            raise ValueError("Capacity must greater than zero")
        
        self.id = uuid4()
        
        self.name = name
        self.description = description
        self.date_range = date_range
        self.location = location
        self.capacity = capacity
        self.status = EventStatus.DRAFT
        
        self.ticket_categories = []
        self.domain_events = []
        self.domain_events.append(EventCreated(self.id))
        
            
    def add_ticket_category(self, category: "TicketCategory"):
            current_total_quota = sum(c.quota for c in self.ticket_categories)
            if current_total_quota + category.quota > self.capacity:
                raise ValueError(f"Total quota ({current_total_quota + category.quota}) exceeds event capacity ({self.capacity})")
            
            self.ticket_categories.append(category)
    
    def publish(self):
        if self.status != EventStatus.DRAFT:
            raise ValueError("only draft event can be published")
        self.status = EventStatus.PUBLISHED
        
        if not self.ticket_categories:
            raise ValueError("Cannot publish event without at least one ticket category")
        
        self.domain_events.append(EventPublished(self.id))
    
    def cancel(self):
        self.status = EventStatus.CANCELLED
        self.domain_events.append(EventCancelled(self.id))
        
        