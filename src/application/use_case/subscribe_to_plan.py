from uuid import UUID

from pydantic import BaseModel

from src.application.exceptions import (
    PlanNotFoundError,
    SubscriptionConflictError,
    UserNotFoundError,
)
from src.domain.entity import Subscription


class SubscribeToPlanInputDTO(BaseModel):
    """
    Input DTO for subscribing to a plan.
    """

    user_id: UUID
    plan_id: UUID
    payment_token: str


class SubscribeToPlanOutputDTO(BaseModel):
    """
    Output DTO for subscribing to a plan.
    """

    subscription_id: UUID


class SubscribeToPlanUseCase:
    """
    Use case for subscribing to a plan.
    """

    def __init__(
        self,
        subscription_repository,
        user_repository,
        plan_repository,
        payment_gateway,
        notification_service,
    ) -> None:
        """
        Initialize the use case.
        """

        self._subscription_repository = subscription_repository
        self._user_repository = user_repository
        self._plan_repository = plan_repository
        self._payment_gateway = payment_gateway
        self._notification_service = notification_service

    def execute(self, input_dto: SubscribeToPlanInputDTO) -> SubscribeToPlanOutputDTO:
        """
        Execute the use case.
        """

        user = self._user_repository.get_by_id(input_dto.user_id)
        if not user:
            raise UserNotFoundError("User does not exists")

        plan = self._plan_repository.get_by_id(input_dto.plan_id)
        if not plan:
            raise PlanNotFoundError("Plan not found")

        subscription = self._subscription_repository.get_by_user_id(
            user_id=input_dto.user_id
        )
        if subscription and subscription.is_active:
            raise SubscriptionConflictError("User already has active subscription")

        payment = self._payment_gateway.process_payment(
            payment_token=input_dto.payment_token,
            billing_address=user.billing_address,
        )
        if payment.success:
            subscription = Subscription.create_regular(
                user_id=input_dto.user_id,
                plan_id=input_dto.plan_id,
            )
        else:
            self._notification_service.notify(
                message="Payment failed",
                recipient=user.email,
            )
            subscription = Subscription.create_trial(
                user_id=input_dto.user_id,
                plan_id=input_dto.plan_id,
            )

        self._subscription_repository.save(subscription)
        return SubscribeToPlanOutputDTO(subscription_id=subscription.id)
