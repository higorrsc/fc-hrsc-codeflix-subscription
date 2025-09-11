from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from src.domain.entity import UserAccount


class UserAccountRepository(ABC):
    """
    Abstract class for User Account Repository.
    """

    @abstractmethod
    def save(self, user_account: UserAccount) -> None:
        """
        Save a user account.
        """

        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, user_id: UUID) -> Optional[UserAccount]:
        """
        Get a user account by its ID.
        """

        raise NotImplementedError
