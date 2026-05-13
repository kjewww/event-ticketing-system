from datetime import datetime
from uuid import uuid4

from value_objects.date_range import DateRange
from value_objects.event_status import EventStatus

from events.event_created import EventCreated
from events.event_published import EventPublished
from events.event_cancelled import EventCancelled

from entities.ticket_category import TicketCategory

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
        
        self.domain_events = []
        self.domain_events.append(EventCreated(self.id))
        
        self.ticket_categories = []
        
        def publish():
            if self.status != EventStatus.DRAFT:
                raise ValueError("only draft event can be published")
            self.status = EventStatus.PUBLISHED
            
            self.domain_events.append(EventPublished(self.id))
        
        def cancel():
            self.status = EventStatus.CANCELLED
            self.domain_events.append(EventCancelled(self.id))
        
        