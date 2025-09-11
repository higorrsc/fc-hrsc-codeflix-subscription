from unittest.mock import create_autospec
from uuid import uuid4

import pytest

from src.application.use_case import RenewSubscriptionInputDTO, RenewSubscriptionUseCase
from src.domain.entity import Address, Subscription, UserAccount
from src.infra.notification import NotificationService
from src.infra.payment import Payment, PaymentGateway
from src.infra.repository import (
    InMemorySubscriptionRepository,
    InMemoryUserAccountRepository,
)


@pytest.fixture
def user_account() -> UserAccount:
    """Fixture for creating a user account."""
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
def regular_subscription(user_account: UserAccount) -> Subscription:
    """Fixture for creating a regular subscription."""
    return Subscription.create_regular(
        user_id=user_account.id,
        plan_id=uuid4(),  # type: ignore
    )


@pytest.fixture
def trial_subscription(user_account: UserAccount) -> Subscription:
    """Fixture for creating a trial subscription."""
    return Subscription.create_trial(
        user_id=user_account.id,
        plan_id=uuid4(),  # type: ignore
    )


class TestRenewSubscriptionUseCase:
    """Test cases for renewing a subscription."""

    def test_when_subscription_not_found_then_raise_error(
        self, user_account: UserAccount
    ):
        """Test that when subscription is not found, it notifies and returns None."""
        subscription_repo = InMemorySubscriptionRepository()
        user_account_repo = InMemoryUserAccountRepository(user_accounts=[user_account])
        payment_gateway = create_autospec(PaymentGateway)
        notification_service = create_autospec(NotificationService)

        use_case = RenewSubscriptionUseCase(
            subscription_repository=subscription_repo,
            user_account_repository=user_account_repo,
            payment_gateway=payment_gateway,
            notification_service=notification_service,
        )

        input_dto = RenewSubscriptionInputDTO(
            subscription_id=uuid4(),
            payment_token="token",
        )

        output = use_case.execute(input_dto)

        assert output is None
        notification_service.notify.assert_called_once_with(
            message="Subscription not found",
            recipient=None,
        )

    def test_when_payment_succeeds_and_subscription_is_regular_then_renew(
        self,
        regular_subscription: Subscription,
        user_account: UserAccount,
    ):
        """Test when payment succeeds for a regular subscription, it gets renewed."""
        subscription_repo = InMemorySubscriptionRepository(
            subscriptions=[regular_subscription]
        )
        user_account_repo = InMemoryUserAccountRepository(user_accounts=[user_account])
        payment_gateway = create_autospec(PaymentGateway)
        payment_gateway.process_payment.return_value = Payment(success=True)
        notification_service = create_autospec(NotificationService)

        use_case = RenewSubscriptionUseCase(
            subscription_repository=subscription_repo,
            user_account_repository=user_account_repo,
            payment_gateway=payment_gateway,
            notification_service=notification_service,
        )

        input_dto = RenewSubscriptionInputDTO(
            subscription_id=regular_subscription.id,
            payment_token="token",
        )
        output = use_case.execute(input_dto)

        assert output is not None
        assert output.subscription_id == regular_subscription.id

        updated_subscription = subscription_repo.get_by_id(regular_subscription.id)
        assert updated_subscription is not None
        assert updated_subscription.is_active is True
        assert updated_subscription.is_trial is False

        payment_gateway.process_payment.assert_called_once_with(
            payment_token=input_dto.payment_token,
            billing_address=user_account.billing_address,
        )
        notification_service.notify.assert_not_called()

    def test_when_payment_fails_and_subscription_is_regular_then_convert_to_trial(
        self,
        regular_subscription: Subscription,
        user_account: UserAccount,
    ):
        """Test when payment fails for a regular subscription, it converts to trial."""
        subscription_repo = InMemorySubscriptionRepository(
            subscriptions=[regular_subscription]
        )
        user_account_repo = InMemoryUserAccountRepository(user_accounts=[user_account])
        payment_gateway = create_autospec(PaymentGateway)
        payment_gateway.process_payment.return_value = Payment(success=False)
        notification_service = create_autospec(NotificationService)

        use_case = RenewSubscriptionUseCase(
            subscription_repository=subscription_repo,
            user_account_repository=user_account_repo,
            payment_gateway=payment_gateway,
            notification_service=notification_service,
        )

        input_dto = RenewSubscriptionInputDTO(
            subscription_id=regular_subscription.id,
            payment_token="token",
        )
        output = use_case.execute(input_dto)

        assert output is not None
        assert output.subscription_id == regular_subscription.id

        updated_subscription = subscription_repo.get_by_id(regular_subscription.id)
        assert updated_subscription is not None
        assert updated_subscription.is_trial is True
        notification_service.notify.assert_called_once_with(
            message=f"Payment failed for subscription {input_dto.subscription_id}",
            recipient=user_account.email,
        )

    def test_when_payment_fails_and_subscription_is_trial_then_cancel(
        self, trial_subscription: Subscription, user_account: UserAccount
    ):
        """Test when payment fails for a trial subscription, it gets cancelled."""
        subscription_repo = InMemorySubscriptionRepository(
            subscriptions=[trial_subscription]
        )
        user_account_repo = InMemoryUserAccountRepository(user_accounts=[user_account])
        payment_gateway = create_autospec(PaymentGateway)
        payment_gateway.process_payment.return_value = Payment(success=False)
        notification_service = create_autospec(NotificationService)

        use_case = RenewSubscriptionUseCase(
            subscription_repository=subscription_repo,
            user_account_repository=user_account_repo,
            payment_gateway=payment_gateway,
            notification_service=notification_service,
        )

        input_dto = RenewSubscriptionInputDTO(
            subscription_id=trial_subscription.id,
            payment_token="token",
        )
        use_case.execute(input_dto)

        updated_subscription = subscription_repo.get_by_id(trial_subscription.id)
        assert updated_subscription is not None
        assert updated_subscription.is_cancelled is True
        notification_service.notify.assert_called_once_with(
            message=f"Payment failed for subscription {input_dto.subscription_id}",
            recipient=user_account.email,
        )
