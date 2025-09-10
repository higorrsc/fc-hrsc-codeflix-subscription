from abc import ABC, abstractmethod
from typing import Optional


class NotificationService(ABC):
    """
    Abstract base class for notification services.
    """

    @abstractmethod
    def notify(self, message: str, recipient: Optional[str]) -> None:
        """
        Send a notification with the given message

        Args:
            message: The notification message
            recipient: Optional recipient identifier (email, phone, etc.)
        """

        pass
