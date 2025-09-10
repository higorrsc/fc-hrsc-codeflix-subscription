from typing import List, Optional
from uuid import UUID

from src.application.exceptions import SubscriptionAlreadyExistsError
from src.domain.subscription import Subscription


class InMemorySubscriptionRepository:
    """
    In-memory repository for managing subscriptions.
    """

    def __init__(self, subscriptions: Optional[List[Subscription]] = None) -> None:
        """
        Initialize the repository with an optional list of subscriptions.
        """

        self._subscriptions = subscriptions or []

    def get_by_id(self, subscription_id: UUID) -> Optional[Subscription]:
        """
        Get a subscription by its ID.
        """

        for subscription in self._subscriptions:
            if subscription.id == subscription_id:
                return subscription

        return None

    def save(self, subscription: Subscription):
        """
        Save a subscription.
        """

        if self.get_by_id(subscription.id):
            raise SubscriptionAlreadyExistsError(
                f"Subscription with id '{subscription.id}' already exists."
            )

        self._subscriptions.append(subscription)

    def update(self, subscription: Subscription):
        """
        Update a subscription.
        """

        for i, s in enumerate(self._subscriptions):
            if s.id == subscription.id:
                self._subscriptions[i] = subscription
                break

    def get_by_user_id_and_plan_id(
        self,
        user_id: UUID,
        plan_id: UUID,
    ) -> Optional[Subscription]:
        """
        Get a subscription by user ID and plan ID.
        """

        for subscription in self._subscriptions:
            if subscription.user_id == user_id and subscription.plan_id == plan_id:
                return subscription

        return None

    def get_by_user_id(self, user_id: UUID) -> Optional[Subscription]:
        """
        Get all subscriptions by user ID.
        """

        for subscription in self._subscriptions:
            if subscription.user_id == user_id:
                return subscription

        return None

    def get_by_plan_id(self, plan_id: UUID) -> Optional[Subscription]:
        """
        Get all subscriptions by plan ID.
        """

        for subscription in self._subscriptions:
            if subscription.plan_id == plan_id:
                return subscription

        return None
