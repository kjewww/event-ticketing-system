from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.infrastructure.database.database import Base


class BookingModel(Base):
    __tablename__ = "bookings"

    id = Column(UUID(as_uuid=True), primary_key=True)

    customer_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    customer_name = Column(String(255), nullable=False, default="")

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

    quantity = Column(Integer, nullable=False)

    unit_price_amount = Column(Numeric(12, 2), nullable=False)
    unit_price_currency = Column(String(10), nullable=False, default="IDR")

    service_fee_amount = Column(Numeric(12, 2), nullable=False, default=0)
    service_fee_currency = Column(String(10), nullable=False, default="IDR")

    total_price_amount = Column(Numeric(12, 2), nullable=False)
    total_price_currency = Column(String(10), nullable=False, default="IDR")

    payment_deadline_at = Column(DateTime, nullable=False)

    status = Column(String(50), nullable=False, index=True)
    refund_required = Column(Boolean, nullable=False, default=False)

    event = relationship(
        "EventModel",
        back_populates="bookings",
    )

    ticket_category = relationship(
        "TicketCategoryModel",
        back_populates="bookings",
    )

    tickets = relationship(
        "TicketModel",
        back_populates="booking",
        cascade="all, delete-orphan",
    )