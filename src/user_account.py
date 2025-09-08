from pydantic import EmailStr

from src.entity import Entity
from src.value_objects import ValueObject


class Address(ValueObject):
    """
    Model representing a physical address.

    Attributes:
        street (str): The street name.
        city (str): The city name.
        state (str): The state name.
        zip_code (str): The zip code.
        country (str): The country name.
    """

    street: str
    city: str
    state: str
    zip_code: str
    country: str


class UserAccount(Entity):
    """
    Model representing a user account.

    Attributes:
        iam_user_id (str): The IAM user ID.
        name (str): The user's full name.
        email (EmailStr): The user's email address.
        billing_address (Address): The user's billing address.
    """

    iam_user_id: str
    name: str
    email: EmailStr
    billing_address: Address
