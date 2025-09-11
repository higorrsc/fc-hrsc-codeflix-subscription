from uuid import uuid4

from src.domain.entity import Address, UserAccount
from src.infra.repository import InMemoryUserAccountRepository


class TestInMemoryUserAccountRepository:
    """
    Test cases for the InMemoryUserAccountRepository.
    """

    def test_save_and_get_by_id(self):
        """
        Test saving a user account and retrieving it by ID.
        """

        repo = InMemoryUserAccountRepository()
        user_account = UserAccount(
            name="John Doe",
            email="john.doe@example.com",
            iam_user_id="iam_123",
            billing_address=Address(
                street="123 Main St",
                city="Anytown",
                state="CA",
                zip_code="12345",
                country="USA",
            ),
        )
        repo.save(user_account)

        found_user_account = repo.get_by_id(user_account.id)
        assert found_user_account is not None
        assert found_user_account.id == user_account.id
        assert found_user_account.name == user_account.name
        assert found_user_account.email == user_account.email

    def test_get_by_id_not_found(self):
        """
        Test retrieving a user account that does not exist.
        """

        repo = InMemoryUserAccountRepository()
        found_user_account = repo.get_by_id(uuid4())
        assert found_user_account is None

    def test_initialization_with_user_accounts(self):
        """
        Test initializing the repository with an existing list of user accounts.
        """

        user_account1 = UserAccount(
            name="Jane Doe",
            email="jane.doe@example.com",
            iam_user_id="iam_456",
            billing_address=Address(
                street="456 Oak Ave",
                city="Otherville",
                state="NY",
                zip_code="67890",
                country="USA",
            ),
        )

        repo = InMemoryUserAccountRepository([user_account1])

        found_user_account = repo.get_by_id(user_account1.id)
        assert found_user_account is not None
