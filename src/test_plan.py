from src.plan import Plan
from src.value_objects import Currency, MonetaryValue


def test_create_plan_with_name_and_price():
    plan = Plan(name="Basic", price=MonetaryValue(amount=100, currency=Currency.BRL))  # type: ignore

    assert plan.id is not None
    assert plan.name == "Basic"
    assert plan.price.amount == 100
    assert plan.price.currency == Currency.BRL


def test_raise_error_for_invalid_currency():
    try:
        plan = Plan(name="Basic", price=MonetaryValue(amount=100, currency="ABC"))  # type: ignore
    except ValueError as e:
        assert "Input should be 'BRL' or 'USD'" in str(e)
    else:
        assert False, "ValueError not raised"
