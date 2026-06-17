from abc import ABC, abstractmethod
from uuid import UUID

from src.application.dto.report_dto import (
    EventParticipantDTO,
    EventSalesReportDTO,
)


class ReportReadRepository(ABC):
    @abstractmethod
    def get_event_sales_report(
        self,
        event_id: UUID,
    ) -> EventSalesReportDTO:
        pass

    @abstractmethod
    def get_event_participants(
        self,
        event_id: UUID,
    ) -> list[EventParticipantDTO]:
        pass