from typing import Optional

from src.infra.notification import NotificationService


class ConsoleNotificationService(NotificationService):
    """
    A simple notification service that just prints to console
    """

    def notify(self, message: str, recipient: Optional[str] = None) -> None:
        """
        Notify a message to a recipient.

        Args:
            message: The message to notify
            recipient: Optional recipient identifier (email, phone, etc.)
        """
        recipient_info = f" to {recipient}" if recipient else ""
        print(f"NOTIFICATION{recipient_info}: {message}")
