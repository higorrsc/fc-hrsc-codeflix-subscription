from unittest.mock import create_autospec

import pytest

from src.application.create_user_account import (
    CreateUserAccountInputDTO,
    CreateUserAccountUseCase,
)
from src.application.exceptions import UserAlreadyExistsError
from src.domain.user_account import Address
from src.infra.auth_service import AuthService
from src.infra.in_memory_user_account_repository import InMemoryUserAccountRepository

account_input = CreateUserAccountInputDTO(
    name="John McLean",
    email="john.mclean@examplepetstore.com",
    password="password",  # type: ignore
    billing_address=Address(
        street="123 Main St",
        city="Anytown",
        state="CA",
        zip_code="12345",
        country="USA",
    ),
)


class TestCreateUserAccount:
    """
    Test cases for creating a user account.
    """

    def test_when_email_is_registered_in_auth_service_then_raises_exception(
        self,
    ) -> None:
        """
        Test when email is already registered in auth service then raises exception.
        """

        mock_auth_service = create_autospec(AuthService)
        mock_auth_service.find_by_email.return_value = "john.mclean@examplepetstore.com"

        use_case = CreateUserAccountUseCase(
            auth_service=mock_auth_service,
            repository=None,  # Repository is not needed for this test
        )

        with pytest.raises(UserAlreadyExistsError):
            use_case.execute(input_dto=account_input)

    def test_when_user_does_not_exist_then_create_user_account_with_iam_id(
        self,
    ) -> None:
        """
        Test when user does not exist then create user account.
        """

        mock_auth_service = create_autospec(AuthService)
        mock_auth_service.find_by_email.return_value = None
        mock_auth_service.create_user.return_value = "iam_user_id"

        repo = InMemoryUserAccountRepository()

        use_case = CreateUserAccountUseCase(
            auth_service=mock_auth_service,
            repository=repo,
        )

        output = use_case.execute(input_dto=account_input)
        assert output.user_id is not None
        assert output.iam_user_id == "iam_user_id"

        mock_auth_service.create_user.assert_called_once_with(
            email=account_input.email,
            password=account_input.password.get_secret_value(),
        )
