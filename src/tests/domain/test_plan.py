from src.domain._shared.value_objects import Currency, MonetaryValue
from src.domain.plan import Plan


def test_create_plan_with_name_and_price():
    """
    Test the creation of a Plan with a valid name and price.
    """

    plan = Plan(
        name="Basic",
        price=MonetaryValue(
            amount=100,  # type: ignore
            currency=Currency.BRL,
        ),
    )

    assert plan.id is not None
    assert plan.name == "Basic"
    assert plan.price.amount == 100
    assert plan.price.currency == Currency.BRL


def test_raise_error_for_invalid_currency():
    """
    Test that creating a Plan with an invalid currency raises a ValueError.
    """
    try:
        plan = Plan(
            name="Basic",
            price=MonetaryValue(
                amount=100,  # type: ignore
                currency="ABC",  # type: ignore
            ),
        )
    except ValueError as e:
        assert "Input should be 'BRL' or 'USD'" in str(e)
    else:
        assert False, "ValueError not raised"
