from sqlalchemy import Column, DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.infrastructure.database.database import Base


class TicketModel(Base):
    __tablename__ = "tickets"

    id = Column(UUID(as_uuid=True), primary_key=True)

    booking_id = Column(
        UUID(as_uuid=True),
        ForeignKey("bookings.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    event_id = Column(
        UUID(as_uuid=True),
        ForeignKey("events.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    ticket_category_id = Column(
        UUID(as_uuid=True),
        ForeignKey("ticket_categories.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    ticket_code = Column(String(100), nullable=False, unique=True, index=True)
    status = Column(String(50), nullable=False, index=True)
    checked_in_at = Column(DateTime, nullable=True)

    booking = relationship(
        "BookingModel",
        back_populates="tickets",
    )

    ticket_category = relationship(
        "TicketCategoryModel",
        back_populates="tickets",
    )

    __table_args__ = (
        UniqueConstraint("ticket_code", name="uq_tickets_ticket_code"),
    )