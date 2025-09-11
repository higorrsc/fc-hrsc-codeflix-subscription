import uuid
from uuid import uuid4

import pytest

from src.application.exceptions import SubscriptionNotFoundError
from src.application.use_case import (
    CancelSubscriptionInputDTO,
    CancelSubscriptionUseCase,
)
from src.domain.entity import Subscription
from src.infra.repository import InMemorySubscriptionRepository

valid_subscription = Subscription.create_regular(
    user_id=uuid.uuid4(),
    plan_id=uuid.uuid4(),
)


class TestCancelSubscription:
    """
    Test cases for canceling a subscription.
    """

    def test_cancel_invalid_subscription_then_raises_exception(self):
        """
        Test that canceling an invalid subscription raises an exception.
        """

        repo = InMemorySubscriptionRepository()
        use_case = CancelSubscriptionUseCase(repository=repo)

        with pytest.raises(SubscriptionNotFoundError, match="Subscription not found"):
            use_case.execute(input_dto=CancelSubscriptionInputDTO(id=uuid4()))

    def test_cancel_valid_subscription(self):
        """
        Test that canceling a valid subscription successfully cancels the subscription.
        """

        repo = InMemorySubscriptionRepository([valid_subscription])
        use_case = CancelSubscriptionUseCase(repository=repo)
        use_case.execute(input_dto=CancelSubscriptionInputDTO(id=valid_subscription.id))

        found_subscription = repo.get_by_id(valid_subscription.id)
        assert found_subscription is not None
        assert found_subscription.is_cancelled
