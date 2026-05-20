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