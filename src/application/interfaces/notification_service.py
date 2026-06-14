from abc import ABC, abstractmethod
from uuid import UUID


class NotificationService(ABC):
    @abstractmethod
    def send(
        self,
        recipient_id: UUID,
        subject: str,
        message: str,
    ) -> None:
        pass