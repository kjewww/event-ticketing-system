from abc import ABC, abstractmethod

from src.domain.value_objects.ticket_code import TicketCode


class TicketCodeGenerator(ABC):
    @abstractmethod
    def generate_many(self, quantity: int) -> list[TicketCode]:
        pass