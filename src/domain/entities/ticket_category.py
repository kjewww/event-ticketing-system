from src.domain.value_objects.date_range import DateRange
from src.domain.value_objects.money import Money
from uuid import uuid4


class TicketCategory:
    def __init__(
        self,
        name: str,
        price: Money,
        quota: int,
        sales_date_range: DateRange
        ):
        
        if quota <= 0:
            raise ValueError("Quota must be greater than zero!")
                
        self.id = uuid4()
        self.name = name
        self.price = price
        self.quota = quota
        self.sales_date_range = sales_date_range
        self.is_active: bool = True
        
    def disable(self):
        self.is_active = False