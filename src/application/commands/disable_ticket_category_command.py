from uuid import UUID


class DisableTicketCategoryCommand:
    def __init__(
        self,
        event_id: UUID,
        organizer_id: str,
        ticket_category_id: UUID,
    ):
        self.event_id = event_id
        self.organizer_id = organizer_id
        self.ticket_category_id = ticket_category_id