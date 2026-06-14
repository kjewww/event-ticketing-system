from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.infrastructure.database.database import Base


class EventModel(Base):
    __tablename__ = "events"

    id = Column(UUID(as_uuid=True), primary_key=True)
    organizer_id = Column(UUID(as_uuid=True), nullable=False, index=True)

    name = Column(String(255), nullable=False)
    description = Column(String, nullable=False)
    location = Column(String(255), nullable=False)

    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    capacity = Column(Integer, nullable=False)
    status = Column(String(50), nullable=False, index=True)

    ticket_categories = relationship(
        "TicketCategoryModel",
        back_populates="event",
        cascade="all, delete-orphan",
    )

    bookings = relationship(
        "BookingModel",
        back_populates="event",
    )