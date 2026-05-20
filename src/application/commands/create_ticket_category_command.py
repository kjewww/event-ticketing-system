from datetime import date, datetime
from decimal import Decimal
from uuid import UUID


class CreateTicketCategoryCommand:
    def __init__(
        self,
        event_id: UUID,
        organizer_id: str,
        name: str,
        price_amount: Decimal,
        quota: int,
        sales_start_date: date | datetime,
        sales_end_date: date | datetime,
        currency: str = "IDR",
    ):
        self.event_id = event_id
        self.organizer_id = organizer_id
        self.name = name
        self.price_amount = price_amount
        self.currency = currency
        self.quota = quota
        self.sales_start_date = sales_start_date
        self.sales_end_date = sales_end_date