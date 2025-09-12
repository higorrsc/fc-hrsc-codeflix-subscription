from datetime import datetime
from uuid import UUID

from sqlmodel import Field, SQLModel

from src.domain.entity import SubscriptionStatus
from src.domain.entity.subscription import Subscription


class SubscriptionModel(SQLModel, table=True):
    """
    Defines a model that represents a subscription
    """

    __tablename__ = "subscriptions"  # type: ignore

    id: UUID = Field(primary_key=True)
    user_id: UUID = Field(foreign_key="user_accounts.id", index=True)
    plan_id: UUID = Field(foreign_key="plans.id", index=True)
    start_date: datetime
    end_date: datetime
    is_trial: bool = Field(default=False)
    status: str = Field(default=SubscriptionStatus.ACTIVE)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    is_active: bool = Field(default=True)

    @classmethod
    def from_entity(cls, subscription: Subscription) -> "SubscriptionModel":
        """
        Transform a Subscription Entity in a Subscription Model
        """

        return cls(
            id=subscription.id,
            user_id=subscription.user_id,
            plan_id=subscription.plan_id,
            start_date=subscription.start_date,
            end_date=subscription.end_date,
            status=subscription.status,
            is_trial=subscription.is_trial,
            created_at=subscription.created_at,
            updated_at=subscription.updated_at,
        )

    @classmethod
    def to_entity(cls, subscription_model: "SubscriptionModel") -> Subscription:
        """
        Transform a Subscription Model in a Subscription Entity
        """

        return Subscription(
            id=subscription_model.id,
            user_id=subscription_model.user_id,
            plan_id=subscription_model.plan_id,
            start_date=subscription_model.start_date,
            end_date=subscription_model.end_date,
            status=SubscriptionStatus(subscription_model.status),
            is_trial=subscription_model.is_trial,
            created_at=subscription_model.created_at,
            updated_at=subscription_model.updated_at,
        )
