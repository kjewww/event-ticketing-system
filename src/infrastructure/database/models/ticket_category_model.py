from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.infrastructure.database.database import Base


class TicketCategoryModel(Base):
    __tablename__ = "ticket_categories"

    id = Column(UUID(as_uuid=True), primary_key=True)
    event_id = Column(
        UUID(as_uuid=True),
        ForeignKey("events.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    name = Column(String(100), nullable=False)

    price_amount = Column(Numeric(12, 2), nullable=False)
    price_currency = Column(String(10), nullable=False, default="IDR")

    quota = Column(Integer, nullable=False)

    sales_start_date = Column(Date, nullable=False)
    sales_end_date = Column(Date, nullable=False)

    is_active = Column(Boolean, nullable=False, default=True)

    event = relationship(
        "EventModel",
        back_populates="ticket_categories",
    )

    bookings = relationship(
        "BookingModel",
        back_populates="ticket_category",
    )

    tickets = relationship(
        "TicketModel",
        back_populates="ticket_category",
    )