from src.application.exceptions import DuplicatePlanError
from src.application.use_case import (
    CreatePlanInputDTO,
    CreatePlanOutputDTO,
    CreatePlanUseCase,
)
from src.domain._shared import Currency, MonetaryValue
from src.domain.entity import Plan
from src.infra.repository import InMemoryPlanRepository


class TestCreatePlan:
    """
    Test cases for creating a plan.
    """

    def test_when_plan_with_name_exists_then_return_error(self):
        """
        Test that creating a plan with an existing name returns an error.
        """

        basic_plan = Plan(
            name="Basic",
            price=MonetaryValue(
                amount=29.90,  # type: ignore
                currency=Currency.BRL,
            ),
        )

        repo = InMemoryPlanRepository()
        repo.save(basic_plan)

        try:
            use_case = CreatePlanUseCase(repository=repo)
            use_case.execute(
                CreatePlanInputDTO(
                    name="Basic",
                    price=MonetaryValue(
                        amount=29.90,  # type: ignore
                        currency=Currency.BRL,
                    ),
                )
            )
        except DuplicatePlanError as e:
            assert str(e) == "Plan with name 'Basic' already exists."

    def test_when_plan_with_name_does_not_exist_then_create_plan(self):
        """
        Test that creating a plan with a new name successfully creates the plan.
        """

        basic_plan = Plan(
            name="Basic",
            price=MonetaryValue(
                amount=29.90,  # type: ignore
                currency=Currency.BRL,
            ),
        )

        repo = InMemoryPlanRepository()
        repo.save(basic_plan)

        try:
            use_case = CreatePlanUseCase(repository=repo)
            use_case.execute(
                CreatePlanInputDTO(
                    name="Plus",
                    price=MonetaryValue(
                        amount=59.90,  # type: ignore
                        currency=Currency.BRL,
                    ),
                )
            )
        except DuplicatePlanError as e:
            assert str(e) == "Plan with name 'Basic' already exists."

    def test_create_plan(self):
        """
        Test that creating a plan with a new name successfully creates the plan.
        """

        repo = InMemoryPlanRepository()

        use_case = CreatePlanUseCase(repository=repo)
        output: CreatePlanOutputDTO = use_case.execute(
            CreatePlanInputDTO(
                name="Plus",
                price=MonetaryValue(
                    amount=59.90,  # type: ignore
                    currency=Currency.BRL,
                ),
            )
        )

        plan = repo.find_by_name("Plus")
        assert plan is not None

        assert output.id is not None
        assert output.name == "Plus"
        assert output.price == MonetaryValue(
            amount=59.90,  # type: ignore
            currency=Currency.BRL,
        )
