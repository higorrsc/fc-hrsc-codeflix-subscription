from abc import ABC, abstractmethod

from src.domain._shared import ValueObject
from src.domain.entity import Address


class Payment(ValueObject):
    """
    Model representing a payment.

    Attributes:
        success (bool): Indicates if the payment was successful.
    """

    success: bool


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
