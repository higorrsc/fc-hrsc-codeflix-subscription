from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlmodel import Session, select

from src.domain.entity import Subscription
from src.domain.repository import SubscriptionRepository
from src.infra.db.models import SubscriptionModel


class SQLModelSubscriptionRepository(SubscriptionRepository):
    """
    Class that represents a repository for subscriptions.
    It implements the SubscriptionRepository interface.
    """

    def __init__(self, session: Session):
        """
        Constructor
        """

        self.session = session

    def get_by_id(self, subscription_id: UUID) -> Optional[Subscription]:
        """
        Get a subscription by ID.
        """

        statement = select(SubscriptionModel).where(
            SubscriptionModel.id == subscription_id
        )
        result = self.session.exec(statement).first()
        return SubscriptionModel.to_entity(result) if result else None

    def get_by_user_id(self, user_id: UUID) -> Optional[Subscription]:
        """
        Get a subscription by user ID.
        """

        statement = select(SubscriptionModel).where(
            SubscriptionModel.user_id == user_id
        )
        result = self.session.exec(statement).first()
        return SubscriptionModel.to_entity(result) if result else None

    def get_by_plan_id(self, plan_id: UUID) -> Optional[Subscription]:
        """
        Get a subscription by plan ID.
        """

        statement = select(SubscriptionModel).where(
            SubscriptionModel.plan_id == plan_id
        )
        result = self.session.exec(statement).first()
        return SubscriptionModel.to_entity(result) if result else None

    def get_by_user_id_and_plan_id(
        self,
        user_id: UUID,
        plan_id: UUID,
    ) -> Optional[Subscription]:
        """
        Get a subscription by user ID and plan ID.
        """

        statement = select(SubscriptionModel).where(
            SubscriptionModel.plan_id == plan_id,
            SubscriptionModel.user_id == user_id,
        )
        result = self.session.exec(statement).first()
        return SubscriptionModel.to_entity(result) if result else None

    def save(self, subscription: Subscription) -> None:
        """
        Save a subscription.
        """

        subscription.updated_at = datetime.now()
        model = SubscriptionModel.from_entity(subscription)
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)

    def update(self, subscription: Subscription):
        """
        Update a subscription.
        """

        raise NotImplementedError
