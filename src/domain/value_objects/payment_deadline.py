from datetime import datetime


class PaymentDeadline:
    def __init__(self, deadline_at: datetime):
        self.deadline_at = deadline_at

    def has_passed(self, now: datetime) -> bool:
        return now > self.deadline_at

    def __eq__(self, other):
        if not isinstance(other, PaymentDeadline):
            return False

        return self.deadline_at == other.deadline_at

    def __repr__(self):
        return f"PaymentDeadline(deadline_at={self.deadline_at!r})"