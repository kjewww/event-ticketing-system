from sqlalchemy.orm import declarative_base, relationship, mapped_column, Mapped
from sqlalchemy import Integer, String, Boolean, ForeignKey, Date, Enum
from datetime import date, datetime
from src.domain.value_objects.event_status import EventStatus
from database import Base

class EventModel(Base):
    __tablename__ = 'events'

    id:             Mapped[str] = mapped_column(String, primary_key=True)
    organizer_id:   Mapped[str] = mapped_column(String, nullable=False)
    name:           Mapped[str] = mapped_column(String, nullable=False)
    description:    Mapped[str] = mapped_column(String, nullable=False)
    location:       Mapped[str] = mapped_column(String, nullable=False)
    capacity:       Mapped[int] = mapped_column(Integer, nullable=False)
    status:         Mapped[EventStatus] = mapped_column(Enum(EventStatus), nullable=False)
    start_date:     Mapped[date] = mapped_column(Date, nullable=False)
    end_date:       Mapped[date] = mapped_column(Date, nullable=False)

    ticket_categories: Mapped[list["TicketCategoryModel"]] = relationship(
        "TicketCategoryModel", 
        back_populates="event", 
        cascade="all, delete-orphan"
    )
    
    
class TicketCategoryModel(Base):
    __tablename__ = 'ticket_categories'

    id:                 Mapped[str] = mapped_column(String, primary_key=True)
    event_id:           Mapped[str] = mapped_column(String, ForeignKey('events.id'), nullable=False)
    name:               Mapped[str] = mapped_column(String, nullable=False)
    price:              Mapped[int] = mapped_column(Integer, nullable=False)
    quota:              Mapped[int] = mapped_column(Integer, nullable=False)
    sales_start_date:   Mapped[date] = mapped_column(Date, nullable=False)
    sales_end_date:     Mapped[date] = mapped_column(Date, nullable=False)
    is_active:          Mapped[bool] = mapped_column(Boolean, nullable=False)
    
    event: Mapped["EventModel"] = relationship(
        "EventModel", 
        back_populates="ticket_categories"
    )