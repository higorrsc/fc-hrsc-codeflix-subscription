from uuid import uuid4

import pytest

from src.application.exceptions import SubscriptionAlreadyExistsError
from src.domain.subscription import Subscription, SubscriptionStatus
from src.infra.in_memory_subscription_repository import InMemorySubscriptionRepository


class TestInMemorySubscriptionRepository:
    """
    Test cases for the InMemorySubscriptionRepository.
    """

    def test_save_and_get_by_id(self):
        """
        Test saving a subscription and retrieving it by ID.
        """

        repo = InMemorySubscriptionRepository()
        subscription = Subscription.create_regular(
            user_id=uuid4(),
            plan_id=uuid4(),
        )
        repo.save(subscription)

        found_subscription = repo.get_by_id(subscription.id)
        assert found_subscription is not None
        assert found_subscription.id == subscription.id
        assert found_subscription.user_id == subscription.user_id
        assert found_subscription.plan_id == subscription.plan_id
        assert found_subscription.status == SubscriptionStatus.ACTIVE

    def test_get_by_id_not_found(self):
        """
        Test retrieving a subscription that does not exist.
        """

        repo = InMemorySubscriptionRepository()
        found_subscription = repo.get_by_id(uuid4())
        assert found_subscription is None

    def test_save_duplicate_subscription_id(self):
        """
        Test saving a subscription with an ID that already exists.
        """

        repo = InMemorySubscriptionRepository()
        subscription1 = Subscription.create_regular(
            user_id=uuid4(),
            plan_id=uuid4(),
        )
        repo.save(subscription1)

        subscription2 = Subscription.create_regular(
            user_id=uuid4(),
            plan_id=uuid4(),
        )
        subscription2.id = subscription1.id  # Assign the same ID

        with pytest.raises(
            SubscriptionAlreadyExistsError,
            match=f"Subscription with id '{subscription1.id}' already exists.",
        ):
            repo.save(subscription2)
