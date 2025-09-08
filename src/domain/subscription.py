from datetime import datetime
from enum import StrEnum
from uuid import UUID

from dateutil.relativedelta import relativedelta

from src.domain._shared.entity import Entity


class SubscriptionStatus(StrEnum):
    """
    Enumeration for subscription status.

    Attributes:
        ACTIVE (str): Subscription is active.
        CANCELLED (str): Subscription has been cancelled.
    """

    ACTIVE = "ACTIVE"
    CANCELLED = "CANCELLED"


class Subscription(Entity):
    """
    Subscription entity representing a user's subscription.

    Attributes:
        user_id (UUID): The ID of the user.
        plan_id (UUID): The ID of the subscription plan.
        start_date (datetime): The start date of the subscription.
        end_date (datetime): The end date of the subscription.
        status (SubscriptionStatus): The status of the subscription.
        is_trial (bool): Indicates if the subscription is a trial.
    """

    user_id: UUID
    plan_id: UUID
    start_date: datetime
    end_date: datetime
    status: SubscriptionStatus = SubscriptionStatus.ACTIVE
    is_trial: bool = False

    @property
    def is_expired(self) -> bool:
        """
        Check if the subscription has expired.

        Returns:
            bool: True if the subscription has expired, False otherwise.
        """

        return self.end_date.date() < datetime.now().date()

    @property
    def is_cancelled(self) -> bool:
        """
        Check if the subscription is cancelled.

        Returns:
            bool: True if the subscription is cancelled, False otherwise.
        """

        return self.status == SubscriptionStatus.CANCELLED

    @classmethod
    def create_regular(cls, user_id: UUID, plan_id: UUID) -> "Subscription":
        """
        Create a regular subscription with a 30-day duration.

        Args:
            user_id (UUID): The ID of the user.
            plan_id (UUID): The ID of the subscription plan.

        Returns:
            Subscription: A new regular subscription instance.
        """
        start_date = datetime.now()
        end_date = start_date + relativedelta(days=30)

        return cls(
            user_id=user_id,
            plan_id=plan_id,
            start_date=start_date,
            end_date=end_date,
            status=SubscriptionStatus.ACTIVE,
            is_trial=False,
        )

    @classmethod
    def create_trial(cls, user_id: UUID, plan_id: UUID) -> "Subscription":
        """
        Create a trial subscription with a 7-day duration.

        Args:
            user_id (UUID): The ID of the user.
            plan_id (UUID): The ID of the subscription plan.

        Returns:
            Subscription: A new trial subscription instance.
        """
        start_date = datetime.now()
        end_date = start_date + relativedelta(days=7)

        return cls(
            user_id=user_id,
            plan_id=plan_id,
            start_date=start_date,
            end_date=end_date,
            status=SubscriptionStatus.ACTIVE,
            is_trial=True,
        )

    def renew(self) -> None:
        """
        Renew the subscription.

        If the subscription is a trial, upgrade it to a regular subscription.
        """

        if self.is_cancelled:
            raise ValueError("Cannot renew a cancelled subscription.")

        if self.is_trial:
            self._upgrade()
        else:
            self._extend()

    def cancel(self) -> None:
        """
        Cancel the subscription.
        """

        self.status = SubscriptionStatus.CANCELLED

    def convert_to_trial(self) -> None:
        """
        Convert a regular subscription to a trial subscription.

        Raises:
            ValueError: If the subscription is already a trial.
        """

        if self.is_trial:
            raise ValueError("Subscription is already a trial.")

        self.is_trial = True
        self.start_date = datetime.now()
        self.end_date = self.start_date + relativedelta(days=7)

    def _upgrade(self) -> None:
        """
        Upgrade a trial subscription to a regular subscription.

        Raises:
            ValueError: If the subscription is not a trial.
        """

        if not self.is_trial:
            raise ValueError("Only trial subscriptions can be upgraded.")

        self.is_trial = False
        self.start_date = datetime.now()
        self.end_date = self.start_date + relativedelta(days=30)

    def _extend(self) -> None:
        """
        Extend a regular subscription by 30 days.

        Raises:
            ValueError: If the subscription is a trial.
        """

        if self.is_trial:
            raise ValueError("Trial subscriptions cannot be extended.")

        self.end_date += relativedelta(days=30)
