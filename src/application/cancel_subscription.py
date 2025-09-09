from uuid import UUID

from pydantic import BaseModel

from src.application.exceptions import SubscriptionNotFoundError


class CancelSubscriptionInputDTO(BaseModel):
    """
    Input DTO for canceling a subscription.
    """

    id: UUID


class CancelSubscriptionUseCase:
    """
    Use case for canceling a subscription.
    """

    def __init__(self, repository) -> None:
        """
        Initialize the use case.
        """

        self._repository = repository

    def execute(self, input_dto: CancelSubscriptionInputDTO) -> None:
        """
        Execute the use case.
        """

        subscription = self._repository.get_by_id(input_dto.id)
        if not subscription:
            raise SubscriptionNotFoundError("Subscription not found")

        subscription.cancel()
        self._repository.update(subscription)
