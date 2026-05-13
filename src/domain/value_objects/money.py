from decimal import Decimal


class Money:
    def __init__(
        self,
        amount: Decimal,
        currency: str = "IDR"
    ):
        
        if amount < 0:
            raise ValueError("Amount cannot be negative.")
        
        self.amount = amount
        self.currency = currency
        
    def add(self, other):

        if self.currency != other.currency:
            raise ValueError(
                "Currencies must match."
            )

        return Money(
            self.amount + other.amount,
            self.currency
        )
        
    def multiply(self, quantity: int):

        return Money(
            self.amount * quantity,
            self.currency
        )
        

    def __eq__(self, other):

        return (
            self.amount == other.amount
            and
            self.currency == other.currency
        )
    
    