from abc import ABC, abstractmethod
from typing import Optional


class AuthService(ABC):
    """
    Abstract base class for authentication services.
    """

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[str]:
        """
        Find a user by email.
        """

        raise NotImplementedError

    @abstractmethod
    def create_user(self, email: str, password: str) -> str:
        """
        Create a new user with the given email.
        """

        raise NotImplementedError
