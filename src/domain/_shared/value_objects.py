from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel


class Currency(StrEnum):
    """
    Enumeration of supported currencies.

    Attributes:
        BRL (str): Brazilian Real.
        USD (str): United States Dollar.
    """

    BRL = "BRL"
    USD = "USD"


class ValueObject(BaseModel):
    """
    Base class for value objects.
    """

    model_config = {
        "frozen": True,
    }


class MonetaryValue(ValueObject):
    """
    Model representing a monetary value with amount and currency.

    Attributes:
        amount (Decimal): The monetary amount.
        currency (Currency): The currency of the monetary amount.
    """

    amount: Decimal
    currency: Currency
