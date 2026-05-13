class TicketCode:
    def __init__(self, value: str):
        if not value or not value.strip():
            raise ValueError("Ticket code cannot be empty.")

        self.value = value

    def __eq__(self, other):
        if not isinstance(other, TicketCode):
            return False

        return self.value == other.value

    def __repr__(self):
        return f"TicketCode(value={self.value!r})"