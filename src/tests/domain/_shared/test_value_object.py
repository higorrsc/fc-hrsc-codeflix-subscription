import pytest
from pydantic import ValidationError

from src.domain._shared import Currency, MonetaryValue


def test_equals_compare_attributes():
    mv1 = MonetaryValue(amount=10, currency=Currency.USD)  # type: ignore
    mv2 = MonetaryValue(amount=10, currency=Currency.USD)  # type: ignore

    assert mv1 == mv2


def test_not_equals_different_amount():
    mv1 = MonetaryValue(amount=10, currency=Currency.USD)  # type: ignore
    mv2 = MonetaryValue(amount=20, currency=Currency.USD)  # type: ignore

    assert mv1 != mv2


def test_cannot_mutate_attributes():
    mv = MonetaryValue(amount=100, currency=Currency.USD)  # type: ignore

    with pytest.raises(ValidationError, match="Instance is frozen"):
        mv.amount = 200  # type: ignore

    with pytest.raises(ValidationError, match="Instance is frozen"):
        mv.currency = Currency.BRL
