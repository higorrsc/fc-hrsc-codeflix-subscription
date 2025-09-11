from typing import List, Optional
from uuid import UUID

from src.domain.entity import UserAccount


class InMemoryUserAccountRepository:
    """
    In-memory repository for managing user accounts.
    """

    def __init__(self, user_accounts: Optional[List[UserAccount]] = None) -> None:
        """
        Initialize the repository with an optional list of user accounts.
        """

        self._user_accounts = user_accounts or []

    def save(self, user_account: UserAccount) -> None:
        """
        Save a user account.
        """

        self._user_accounts.append(user_account)

    def get_by_id(self, user_id: UUID) -> Optional[UserAccount]:
        """
        Get a user account by its ID.
        """

        for user_account in self._user_accounts:
            if user_account.id == user_id:
                return user_account

        return None
