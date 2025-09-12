import pytest
from sqlmodel import Session, SQLModel, create_engine

from src.domain._shared.value_objects import Currency, MonetaryValue
from src.domain.entity import Address, Plan, Subscription, UserAccount
from src.infra.db.repository import (
    SQLModelPlanRepository,
    SQLModelSubscriptionRepository,
    SQLModelUserAccountRepository,
)

engine = create_engine("sqlite:///:memory:")


@pytest.fixture
def session():
    """
    Returns a database session.
    """

    SQLModel.metadata.create_all(engine)
    return Session(engine)


class TestSQLModelSubscriptionRepository:
    """
    Test class for SQLModelSubscriptionRepository.
    """

    def test_save_subscription_to_db(self, session):
        """
        Test saving a subscription to the database.
        """

        plan = Plan(
            name="Standard",
            price=MonetaryValue(
                amount=10.0,  # type: ignore
                currency=Currency.BRL,
            ),
        )
        plan_repo = SQLModelPlanRepository(session)
        plan_repo.save(plan)

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
        user_repo = SQLModelUserAccountRepository(session)
        user_repo.save(user)

        repo = SQLModelSubscriptionRepository(session)
        subscription = Subscription.create_regular(
            user_id=user.id,
            plan_id=plan.id,
        )
        repo.save(subscription)

        subscription_from_db = repo.get_by_id(subscription.id)
        assert subscription_from_db

        subscription_from_db_by_user = repo.get_by_user_id(user.id)
        assert subscription_from_db_by_user

        subscription_from_db_by_plan = repo.get_by_plan_id(plan.id)
        assert subscription_from_db_by_plan

        subscription_from_db_by_user_and_plan = repo.get_by_user_id_and_plan_id(
            user_id=user.id,
            plan_id=plan.id,
        )
        assert subscription_from_db_by_user_and_plan
