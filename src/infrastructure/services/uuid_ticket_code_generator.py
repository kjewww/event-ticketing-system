from uuid import uuid4

from src.application.interfaces.ticket_code_generator import TicketCodeGenerator
from src.domain.value_objects.ticket_code import TicketCode


class UUIDTicketCodeGenerator(TicketCodeGenerator):
    def generate_many(self, quantity: int) -> list[TicketCode]:
        if quantity <= 0:
            raise ValueError("Ticket code quantity must be greater than zero.")

        codes: list[TicketCode] = []

        while len(codes) < quantity:
            code = TicketCode(f"TCK-{uuid4().hex[:16].upper()}")

            if code.value not in [existing_code.value for existing_code in codes]:
                codes.append(code)

        return codes