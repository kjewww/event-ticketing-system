from decimal import Decimal


class Money:
    def __init__(
        self,
        amount: Decimal,
        currency: str = "IDR"
    ):
        if not isinstance(amount, Decimal):
            amount = Decimal(str(amount))

        if not currency or not currency.strip():
            raise ValueError("Currency cannot be empty.")
        
        if amount < 0:
            raise ValueError("Amount cannot be negative.")
        
        self.amount = amount
        self.currency = currency
        
    def add(self, other: "Money") -> "Money":
        if not isinstance(other, Money):
            raise TypeError("Can only add Money to Money.")

        if self.currency != other.currency:
            raise ValueError(
                "Currencies must match."
            )

        return Money(
            self.amount + other.amount,
            self.currency
        )
        
    def multiply(self, quantity: int) -> "Money":
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")

        return Money(
            self.amount * quantity,
            self.currency
        )
        

    def __eq__(self, other):
        if not isinstance(other, Money):
            return False

        return (
            self.amount == other.amount
            and
            self.currency == other.currency
        )
    
    def __repr__(self):
        return f"Money(amount={self.amount!r}, currency={self.currency!r})"
    