class CreateEventResponseDTO:
    def __init__(
        self,
        event_id,
        organizer_id,
        name,
        description,
        start_date,
        end_date,
        location,
        capacity,
        status,
    ):
        self.event_id = event_id
        self.organizer_id = organizer_id
        self.name = name
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.location = location
        self.capacity = capacity
        self.status = status


class PublishEventResponseDTO:
    def __init__(
        self,
        event_id,
        name,
        status,
    ):
        self.event_id = event_id
        self.name = name
        self.status = status


class CancelEventResponseDTO:
    def __init__(
        self,
        event_id,
        name,
        status,
    ):
        self.event_id = event_id
        self.name = name
        self.status = status


class AvailableEventDTO:
    def __init__(
        self,
        event_id,
        name,
        start_date,
        end_date,
        location,
        lowest_ticket_price,
    ):
        self.event_id = event_id
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.location = location
        self.lowest_ticket_price = lowest_ticket_price


class EventDetailsDTO:
    def __init__(
        self,
        event_id,
        name,
        description,
        start_date,
        end_date,
        location,
        organizer_id,
        status,
        ticket_categories,
    ):
        self.event_id = event_id
        self.name = name
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.location = location
        self.organizer_id = organizer_id
        self.status = status
        self.ticket_categories = ticket_categories