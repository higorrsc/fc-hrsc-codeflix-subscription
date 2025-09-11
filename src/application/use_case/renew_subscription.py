from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from src.domain.repository import SubscriptionRepository, UserAccountRepository
from src.infra.notification import NotificationService
from src.infra.payment import PaymentGateway


class RenewSubscriptionInputDTO(BaseModel):
    """
    Input DTO for renewing a subscription.
    """

    subscription_id: UUID
    payment_token: str


class RenewSubscriptionOutputDTO(BaseModel):
    """
    Output DTO for renewing a subscription.
    """

    subscription_id: UUID


class RenewSubscriptionUseCase:
    """
    Use case for renewing a subscription.
    """

    def __init__(
        self,
        subscription_repository: SubscriptionRepository,
        user_account_repository: UserAccountRepository,
        payment_gateway: PaymentGateway,
        notification_service: NotificationService,
    ) -> None:
        """
        Initialize the use case.
        """

        self._subscription_repository = subscription_repository
        self._user_account_repository = user_account_repository
        self._payment_gateway = payment_gateway
        self._notification_service = notification_service

    def execute(
        self, input_dto: RenewSubscriptionInputDTO
    ) -> Optional[RenewSubscriptionOutputDTO]:
        """
        Execute the use case.
        """

        subscription = self._subscription_repository.get_by_id(
            input_dto.subscription_id
        )
        if not subscription:
            self._notification_service.notify(
                message="Subscription not found",
                recipient=None,
            )
            return None

        user_account = self._user_account_repository.get_by_id(subscription.user_id)

        payment = self._payment_gateway.process_payment(
            payment_token=input_dto.payment_token,
            billing_address=user_account.billing_address,  # type: ignore
        )

        if payment.success:
            subscription.renew()
        else:
            self._notification_service.notify(
                message=f"Payment failed for subscription {input_dto.subscription_id}",
                recipient=user_account.email,  # type: ignore
            )
            if subscription.is_trial:
                subscription.cancel()
            else:
                subscription.convert_to_trial()

        self._subscription_repository.update(subscription)

        return RenewSubscriptionOutputDTO(subscription_id=subscription.id)
