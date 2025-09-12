import pytest
from sqlmodel import Session, SQLModel, create_engine

from src.domain._shared.value_objects import Currency, MonetaryValue
from src.domain.entity import Plan
from src.infra.db.repository import SQLModelPlanRepository

engine = create_engine("sqlite:///:memory:")


@pytest.fixture
def session():
    """
    Returns a database session.
    """

    SQLModel.metadata.create_all(engine)
    return Session(engine)


class TestSQLModelPlanRepository:
    """
    Test class for SQLModelPlanRepository.
    """

    def test_save_plan_to_db(self, session):
        """
        Test saving a plan to the database.
        """

        repo = SQLModelPlanRepository(session)
        plan = Plan(
            name="Standard",
            price=MonetaryValue(
                amount=10.0,  # type: ignore
                currency=Currency.BRL,
            ),
        )

        repo.save(plan)

        plan_from_db = repo.get_by_id(plan.id)
        assert plan_from_db
