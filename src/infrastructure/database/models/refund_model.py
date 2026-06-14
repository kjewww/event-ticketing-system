from sqlalchemy import Column, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID

from src.infrastructure.database.database import Base


class RefundModel(Base):
    __tablename__ = "refunds"

    id = Column(UUID(as_uuid=True), primary_key=True)

    booking_id = Column(
        UUID(as_uuid=True),
        ForeignKey("bookings.id", ondelete="RESTRICT"),
        nullable=False,
        unique=True,
        index=True,
    )

    customer_id = Column(UUID(as_uuid=True), nullable=False, index=True)

    amount = Column(Numeric(12, 2), nullable=False)
    currency = Column(String(10), nullable=False, default="IDR")

    reason = Column(String, nullable=True)
    status = Column(String(50), nullable=False, index=True)

    rejection_reason = Column(String, nullable=True)
    payment_reference = Column(String(255), nullable=True)