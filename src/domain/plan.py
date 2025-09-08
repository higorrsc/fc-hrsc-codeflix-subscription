from src.domain._shared.entity import Entity
from src.domain._shared.value_objects import MonetaryValue


class Plan(Entity):
    """
    Model representing a plan entity.

    Attributes:
        name (str): The name of the plan.
        price (MonetaryValue): The price of the plan.
    """

    name: str
    price: MonetaryValue
