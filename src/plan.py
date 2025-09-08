from src.entity import Entity
from src.value_objects import MonetaryValue


class Plan(Entity):
    """
    Model representing a plan entity.

    Attributes:
        name (str): The name of the plan.
        price (MonetaryValue): The price of the plan.
    """

    name: str
    price: MonetaryValue
