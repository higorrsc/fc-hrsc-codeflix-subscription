from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, SecretStr

from src.application.exceptions import UserAlreadyExistsError
from src.domain.entity import Address, UserAccount
from src.domain.repository.user_account import UserAccountRepository
from src.infra.auth.auth_service import AuthService


class CreateUserAccountInputDTO(BaseModel):
    """
    Input DTO for creating a user account.
    """

    name: str
    email: EmailStr
    password: SecretStr
    billing_address: Address


class CreateUserAccountOutputDTO(BaseModel):
    """
    Output DTO for creating a user account.
    """

    user_id: UUID
    iam_user_id: str
    name: str
    email: EmailStr
    billing_address: Address
    created_at: datetime
    updated_at: datetime
    is_active: bool


class CreateUserAccountUseCase:
    """
    Use case for creating a user account.
    """

    def __init__(self, auth_service: AuthService, repository: UserAccountRepository):
        """
        Initialize the use case.
        """

        self._auth_service = auth_service
        self._repository = repository

    def execute(
        self, input_dto: CreateUserAccountInputDTO
    ) -> CreateUserAccountOutputDTO:
        """
        Execute the use case.
        """

        iam_user = self._auth_service.find_by_email(input_dto.email)
        if iam_user:
            raise UserAlreadyExistsError("Email is already registered")

        iam_user_id = self._auth_service.create_user(
            email=input_dto.email,
            password=input_dto.password.get_secret_value(),
        )

        user_account = UserAccount(
            name=input_dto.name,
            email=input_dto.email,
            iam_user_id=iam_user_id,
            billing_address=input_dto.billing_address,
        )
        self._repository.save(user_account)

        return CreateUserAccountOutputDTO(
            user_id=user_account.id,
            iam_user_id=user_account.iam_user_id,
            name=user_account.name,
            email=user_account.email,
            billing_address=user_account.billing_address,
            created_at=user_account.created_at,
            updated_at=user_account.updated_at,
            is_active=user_account.is_active,
        )
