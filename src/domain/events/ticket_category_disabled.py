from datetime import datetime

class TicketCategoryDisabled:
    def __init__(self, id):
        self.id = id
        self.occurred_at = datetime.now()