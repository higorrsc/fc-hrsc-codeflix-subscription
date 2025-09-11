from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from src.domain.entity import Subscription


class SubscriptionRepository(ABC):
    """
    Abstract class for Subscription Repository.
    """

    @abstractmethod
    def get_by_id(self, subscription_id: UUID) -> Optional[Subscription]:
        """
        Get a subscription by its ID.
        """

        raise NotImplementedError

    @abstractmethod
    def save(self, subscription: Subscription):
        """
        Save a subscription.
        """

        raise NotImplementedError

    @abstractmethod
    def update(self, subscription: Subscription):
        """
        Update a subscription.
        """

        raise NotImplementedError

    @abstractmethod
    def get_by_user_id_and_plan_id(
        self,
        user_id: UUID,
        plan_id: UUID,
    ) -> Optional[Subscription]:
        """
        Get a subscription by user ID and plan ID.
        """

        raise NotImplementedError

    @abstractmethod
    def get_by_user_id(self, user_id: UUID) -> Optional[Subscription]:
        """
        Get all subscriptions by user ID.
        """

        raise NotImplementedError

    @abstractmethod
    def get_by_plan_id(self, plan_id: UUID) -> Optional[Subscription]:
        """
        Get all subscriptions by plan ID.
        """

        raise NotImplementedError
