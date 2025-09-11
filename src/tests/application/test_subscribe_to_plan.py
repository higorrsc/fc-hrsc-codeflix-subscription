from unittest.mock import create_autospec
from uuid import uuid4

import pytest

from src.application.exceptions import (
    PlanNotFoundError,
    SubscriptionConflictError,
    UserNotFoundError,
)
from src.application.use_case import SubscribeToPlanInputDTO, SubscribeToPlanUseCase
from src.domain._shared import Currency, MonetaryValue
from src.domain.entity import Address, Plan, Subscription, UserAccount
from src.infra.notification.notification_service import NotificationService
from src.infra.payment import Payment, PaymentGateway
from src.infra.repository import (
    InMemoryPlanRepository,
    InMemorySubscriptionRepository,
    InMemoryUserAccountRepository,
)


@pytest.fixture
def user_account() -> UserAccount:
    """
    Fixture for creating a user account.
    """

    return UserAccount(
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


@pytest.fixture
def plan() -> Plan:
    """
    Fixture for creating a plan.
    """

    return Plan(
        name="Basic",
        price=MonetaryValue(
            amount=29.90,  # type: ignore
            currency=Currency.BRL,
        ),
    )


@pytest.fixture
def regular_subscription(
    user_account: UserAccount,
    plan: Plan,
) -> Subscription:
    """
    Fixture for creating a regular subscription.
    """

    return Subscription.create_regular(
        user_id=user_account.id,
        plan_id=plan.id,
    )


@pytest.fixture
def trial_subscription(
    user_account: UserAccount,
    plan: Plan,
) -> Subscription:
    """
    Fixture for creating a trial subscription.
    """

    return Subscription.create_trial(
        user_id=user_account.id,
        plan_id=plan.id,
    )


class TestSubscribeToPlanUseCase:
    """
    Test cases for subscribing to a plan.
    """

    def test_when_payment_succeeds_then_create_regular_subscription(
        self,
        user_account,
        plan,
    ):
        """
        Test when payment succeeds then create regular subscription.
        """

        user_repo = InMemoryUserAccountRepository(user_accounts=[user_account])
        plan_repo = InMemoryPlanRepository(plans=[plan])
        subs_repo = InMemorySubscriptionRepository()
        payment_gateway = create_autospec(PaymentGateway)
        payment_gateway.process_payment.return_value = Payment(success=True)

        use_case = SubscribeToPlanUseCase(
            subscription_repository=subs_repo,
            user_repository=user_repo,
            plan_repository=plan_repo,
            payment_gateway=payment_gateway,
            notification_service=None,
        )
        input_dto = SubscribeToPlanInputDTO(
            user_id=user_account.id,
            plan_id=plan.id,
            payment_token="payment_token_for_test",
        )
        output_dto = use_case.execute(input_dto=input_dto)
        assert output_dto.subscription_id is not None

        created_subscription = subs_repo.get_by_user_id(user_account.id)
        assert created_subscription is not None
        assert created_subscription.is_trial is False

        payment_gateway.process_payment.assert_called_once_with(
            payment_token="payment_token_for_test",
            billing_address=user_account.billing_address,
        )

    def test_when_payment_fails_then_notify_and_create_trial_subscription(
        self,
        user_account,
        plan,
    ):
        """
        Test when payment fails then notify and create trial subscription.
        """

        user_repo = InMemoryUserAccountRepository(user_accounts=[user_account])
        plan_repo = InMemoryPlanRepository(plans=[plan])
        subs_repo = InMemorySubscriptionRepository()
        payment_gateway = create_autospec(PaymentGateway)
        notification_service = create_autospec(NotificationService)
        payment_gateway.process_payment.return_value = Payment(success=False)

        use_case = SubscribeToPlanUseCase(
            subscription_repository=subs_repo,
            user_repository=user_repo,
            plan_repository=plan_repo,
            payment_gateway=payment_gateway,
            notification_service=notification_service,
        )
        input_dto = SubscribeToPlanInputDTO(
            user_id=user_account.id,
            plan_id=plan.id,
            payment_token="payment_token_for_test",
        )
        output_dto = use_case.execute(input_dto=input_dto)
        assert output_dto.subscription_id is not None

        created_subscription = subs_repo.get_by_user_id(user_account.id)
        assert created_subscription is not None
        assert created_subscription.is_trial is True

        payment_gateway.process_payment.assert_called_once_with(
            payment_token="payment_token_for_test",
            billing_address=user_account.billing_address,
        )

    def test_when_user_does_not_exist_then_raise_user_does_not_exists_error(
        self,
        user_account,
        plan,
    ):
        """
        Test when user does not exist then raise user does not exists error.
        """
        user_repo = InMemoryUserAccountRepository(user_accounts=[user_account])
        plan_repo = InMemoryPlanRepository(plans=[plan])
        subs_repo = InMemorySubscriptionRepository()
        payment_gateway = create_autospec(PaymentGateway)
        payment_gateway.process_payment.return_value = Payment(success=False)

        use_case = SubscribeToPlanUseCase(
            subscription_repository=subs_repo,
            user_repository=user_repo,
            plan_repository=plan_repo,
            payment_gateway=payment_gateway,
            notification_service=None,
        )
        input_dto = SubscribeToPlanInputDTO(
            user_id=uuid4(),
            plan_id=plan.id,
            payment_token="payment_token_for_test",
        )

        with pytest.raises(
            UserNotFoundError,
            match="User does not exists",
        ):
            use_case.execute(input_dto=input_dto)

    def test_when_plan_does_not_exist_then_raise_plan_not_found_error(
        self,
        user_account,
        plan,
    ):
        """
        Test when plan does not exist then raise plan not found error.
        """

        user_repo = InMemoryUserAccountRepository(user_accounts=[user_account])
        plan_repo = InMemoryPlanRepository(plans=[plan])
        subs_repo = InMemorySubscriptionRepository()
        payment_gateway = create_autospec(PaymentGateway)
        payment_gateway.process_payment.return_value = Payment(success=False)

        use_case = SubscribeToPlanUseCase(
            subscription_repository=subs_repo,
            user_repository=user_repo,
            plan_repository=plan_repo,
            payment_gateway=payment_gateway,
            notification_service=None,
        )
        input_dto = SubscribeToPlanInputDTO(
            user_id=user_account.id,
            plan_id=uuid4(),
            payment_token="payment_token_for_test",
        )

        with pytest.raises(
            PlanNotFoundError,
            match="Plan not found",
        ):
            use_case.execute(input_dto=input_dto)

    def test_when_user_already_has_active_subscription_then_raise_subscription_conflict_error(
        self,
        user_account,
        plan,
        regular_subscription,
    ):
        """
        Test when user already has active subscription then raise subscription conflict error.
        """

        user_repo = InMemoryUserAccountRepository(user_accounts=[user_account])
        plan_repo = InMemoryPlanRepository(plans=[plan])
        subs_repo = InMemorySubscriptionRepository(subscriptions=[regular_subscription])
        payment_gateway = create_autospec(PaymentGateway)
        payment_gateway.process_payment.return_value = Payment(success=False)

        use_case = SubscribeToPlanUseCase(
            subscription_repository=subs_repo,
            user_repository=user_repo,
            plan_repository=plan_repo,
            payment_gateway=payment_gateway,
            notification_service=None,
        )
        input_dto = SubscribeToPlanInputDTO(
            user_id=user_account.id,
            plan_id=plan.id,
            payment_token="payment_token_for_test",
        )

        with pytest.raises(
            SubscriptionConflictError,
            match="User already has active subscription",
        ):
            use_case.execute(input_dto=input_dto)
