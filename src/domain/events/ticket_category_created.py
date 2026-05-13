from datetime import datetime

class TicketCategoryCreated:
    def __init__(self, ticket_category_id):
        self.ticket_category_id = ticket_category_id
        self.occurred_at = datetime.now()