from uuid import uuid4

from src.domain._shared.value_objects import Currency, MonetaryValue
from src.domain.plan import Plan
from src.infra.in_memory_plan_repository import InMemoryPlanRepository


class TestInMemoryPlanRepository:
    """
    Test cases for the InMemoryPlanRepository.
    """

    def test_save_and_find_by_name(self):
        """
        Test saving a plan and finding it by name.
        """

        repo = InMemoryPlanRepository()
        plan = Plan(
            name="Basic",
            price=MonetaryValue(
                amount=29.90,  # type: ignore
                currency=Currency.BRL,
            ),
        )
        repo.save(plan)

        found_plan = repo.find_by_name("Basic")
        assert found_plan is not None
        assert found_plan.name == "Basic"
        assert found_plan.price == MonetaryValue(
            amount=29.90,  # type: ignore
            currency=Currency.BRL,
        )

    def test_find_by_name_not_found(self):
        """
        Test finding a plan that does not exist.
        """

        repo = InMemoryPlanRepository()
        found_plan = repo.find_by_name("NonExistentPlan")
        assert found_plan is None

    def test_save_duplicate_plan_name(self):
        """
        Test saving a plan with a name that already exists.
        """

        repo = InMemoryPlanRepository()
        plan1 = Plan(
            name="Premium",
            price=MonetaryValue(
                amount=99.90,  # type: ignore
                currency=Currency.BRL,
            ),
        )
        repo.save(plan1)

        plan2 = Plan(
            name="Premium",
            price=MonetaryValue(
                amount=109.90,  # type: ignore
                currency=Currency.BRL,
            ),
        )
        try:
            repo.save(plan2)
            assert False, "ValueError was not raised for duplicate plan name"
        except ValueError as e:
            assert str(e) == "Plan with name 'Premium' already exists."

    def test_initialization_with_plans(self):
        """
        Test initializing the repository with an existing list of plans
        """

        plans = [
            Plan(
                name="Standard",
                price=MonetaryValue(
                    amount=59.90,  # type: ignore
                    currency=Currency.BRL,
                ),
            ),
            Plan(
                name="Enterprise",
                price=MonetaryValue(
                    amount=199.90,  # type: ignore
                    currency=Currency.BRL,
                ),
            ),
        ]
        repo = InMemoryPlanRepository(plans)

        found_standard_plan = repo.find_by_name("Standard")
        assert found_standard_plan is not None
        assert found_standard_plan.name == "Standard"
        assert found_standard_plan.price == MonetaryValue(
            amount=59.90,  # type: ignore
            currency=Currency.BRL,
        )
        found_enterprise_plan = repo.find_by_name("Enterprise")
        assert found_enterprise_plan is not None
        assert found_enterprise_plan.name == "Enterprise"
        assert found_enterprise_plan.price == MonetaryValue(
            amount=199.90,  # type: ignore
            currency=Currency.BRL,
        )

    def test_get_by_id(self):
        """
        Test getting a plan by its ID.
        """

        plan1 = Plan(
            name="Premium",
            price=MonetaryValue(
                amount=99.90,  # type: ignore
                currency=Currency.BRL,
            ),
        )

        plan2 = Plan(
            name="Premium",
            price=MonetaryValue(
                amount=109.90,  # type: ignore
                currency=Currency.BRL,
            ),
        )

        repo = InMemoryPlanRepository([plan1, plan2])
        found_plan = repo.get_by_id(plan1.id)
        assert found_plan is not None
        assert found_plan.id == plan1.id
        assert found_plan.name == plan1.name

    def test_get_by_id_not_found(self):
        """
        Test getting a plan that does not exist.
        """

        repo = InMemoryPlanRepository()
        found_plan = repo.get_by_id(uuid4())
        assert found_plan is None
