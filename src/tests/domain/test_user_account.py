from src.domain.user_account import Address, UserAccount


def test_create_valid_user_account():
    """
    Test creating a valid user account.
    """

    user_account = UserAccount(
        iam_user_id="1234567890123",
        name="John Doe",
        email="john.doe@examplepetstore.com",
        billing_address=Address(
            street="123 Main St",
            city="Anytown",
            state="CA",
            zip_code="12345",
            country="USA",
        ),
    )

    assert user_account.id is not None
