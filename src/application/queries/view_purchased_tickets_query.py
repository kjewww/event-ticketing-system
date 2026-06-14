from uuid import UUID


class ViewPurchasedTicketsQuery:
    def __init__(self, customer_id: UUID):
        self.customer_id = customer_id