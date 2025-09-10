from typing import List, Optional
from uuid import uuid4

from pydantic import EmailStr

from src.infra.auth.auth_service import AuthService


class InMemoryAuthService(AuthService):
    """
    In-memory authentication service for testing purposes.
    """

    def __init__(self, users: Optional[List[str]] = None) -> None:
        """
        Initialize the in-memory auth service with an optional list of users.
        """

        self._users = users or []

    def find_by_email(self, email: EmailStr) -> Optional[str]:
        """
        Find a user by email.
        """

        for user in self._users:
            if user == email:
                return user

        return None

    def create_user(self, email: EmailStr) -> str:
        """
        Create a new user with the given email.
        """

        self._users.append(email)
        return str(uuid4())
