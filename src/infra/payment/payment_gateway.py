import uuid
from abc import ABC, abstractmethod

from pydantic import BaseModel, Field

from src.domain.entity import Address


class Payment(BaseModel):
    """
    Model representing a payment.

    Attributes:
        success (bool): Indicates if the payment was successful.
    """

    success: bool
    transaction_id: uuid.UUID = Field(default_factory=uuid.uuid4)


class PaymentGateway(ABC):
    """
    Abstract base class for payment gateways.
    """

    @abstractmethod
    def process_payment(self, payment_token: str, billing_address: Address) -> Payment:
        """
        Process a payment with the given token.
        """

        raise NotImplementedError
