from datetime import datetime
from uuid import UUID

from sqlmodel import Field, SQLModel

from src.domain.entity.user_account import Address, UserAccount


class UserAccountModel(SQLModel, table=True):
    """
    Defines a model that represents a user account
    """

    __tablename__ = "user_accounts"  # type: ignore

    id: UUID = Field(primary_key=True)
    iam_user_id: str = Field(unique=True)
    name: str
    email: str = Field(unique=True)
    billing_address_street: str = Field()
    billing_address_city: str = Field()
    billing_address_state: str = Field()
    billing_address_zip_code: str = Field()
    billing_address_country: str = Field()
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    is_active: bool = Field(default=True)

    @classmethod
    def from_entity(cls, user: UserAccount) -> "UserAccountModel":
        """
        Transform a User Account Entity in a User Account Model
        """

        return cls(
            id=user.id,
            iam_user_id=user.iam_user_id,
            name=user.name,
            email=user.email,
            billing_address_street=user.billing_address.street,
            billing_address_city=user.billing_address.city,
            billing_address_state=user.billing_address.state,
            billing_address_zip_code=user.billing_address.zip_code,
            billing_address_country=user.billing_address.country,
            created_at=user.created_at,
            updated_at=user.updated_at,
            is_active=user.is_active,
        )

    @classmethod
    def to_entity(cls, user_model: "UserAccountModel") -> UserAccount:
        """
        Transform a User Account Model in a User Account Entity
        """

        return UserAccount(
            id=user_model.id,
            iam_user_id=user_model.iam_user_id,
            name=user_model.name,
            email=user_model.email,
            billing_address=Address(
                street=user_model.billing_address_street,
                city=user_model.billing_address_city,
                state=user_model.billing_address_state,
                zip_code=user_model.billing_address_zip_code,
                country=user_model.billing_address_country,
            ),
            created_at=user_model.created_at,
            updated_at=user_model.updated_at,
            is_active=user_model.is_active,
        )
