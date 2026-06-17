from uuid import UUID

from src.application.interfaces.notification_service import NotificationService


class FakeNotificationService(NotificationService):
    def send(
        self,
        recipient_id: UUID,
        subject: str,
        message: str,
    ) -> None:
        return None