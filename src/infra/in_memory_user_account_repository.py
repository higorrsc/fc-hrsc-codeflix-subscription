from typing import List, Optional

from src.domain.user_account import UserAccount


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
