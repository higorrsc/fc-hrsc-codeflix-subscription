import pytest
from sqlmodel import Session, SQLModel, create_engine

from src.domain.entity import Address, UserAccount
from src.infra.db.repository import SQLModelUserAccountRepository

engine = create_engine("sqlite:///:memory:")


@pytest.fixture
def session():
    """
    Returns a database session.
    """

    SQLModel.metadata.create_all(engine)
    return Session(engine)


class TestSQLModelUserAccountRepository:
    """
    Test class for SQLModelUserAccountRepository.
    """

    def test_save_user_account_to_db(self, session):
        """
        Test saving a plan to the database.
        """

        repo = SQLModelUserAccountRepository(session)
        user = UserAccount(
            iam_user_id="222413ad-97b7-5b86-9e40-c516aea4f4a8",
            name="John Doe",
            email="john.doe@email.com",
            billing_address=Address(
                street="123 Main St",
                city="Anytown",
                state="CA",
                zip_code="12345",
                country="USA",
            ),
        )

        repo.save(user)

        user_from_db = repo.get_by_id(user.id)
        assert user_from_db
