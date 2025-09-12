from typing import Optional
from uuid import UUID

from sqlmodel import Session, select

from src.domain.entity import UserAccount
from src.domain.repository import UserAccountRepository
from src.infra.db.models import UserAccountModel


class SQLModelUserAccountRepository(UserAccountRepository):
    """
    Class that represents a repository for user accounts.
    It implements the UserAccountRepository interface.
    """

    def __init__(self, session: Session):
        """
        Constructor
        """

        self.session = session

    def get_by_id(self, user_id: UUID) -> Optional[UserAccount]:
        """
        Get a user account by ID.
        """

        statement = select(UserAccountModel).where(UserAccountModel.id == user_id)
        result = self.session.exec(statement).first()
        return UserAccountModel.to_entity(result) if result else None

    def get_by_email(self, email: str) -> Optional[UserAccount]:
        """
        Get a user account by email.
        """

        statement = select(UserAccountModel).where(UserAccountModel.email == email)
        result = self.session.exec(statement).first()
        return UserAccountModel.to_entity(result) if result else None

    def save(self, user_account: UserAccount) -> None:
        """
        Save a user account.
        """

        model = UserAccountModel.from_entity(user_account)
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
