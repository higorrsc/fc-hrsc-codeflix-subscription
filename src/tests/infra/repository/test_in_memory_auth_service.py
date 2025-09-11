from src.infra.repository import InMemoryAuthService


class TestInMemoryAuthService:
    """
    Test cases for the InMemoryAuthService.
    """

    def test_find_by_email_existing_user(self):
        """
        Test finding an existing user by email.
        """

        service = InMemoryAuthService(users=["test@example.com"])
        user = service.find_by_email("test@example.com")
        assert user == "test@example.com"

    def test_find_by_email_non_existing_user(self):
        """
        Test finding a non-existing user by email.
        """

        service = InMemoryAuthService()
        user = service.find_by_email("nonexistent@example.com")
        assert user is None

    def test_create_user(self):
        """
        Test creating a new user.
        """

        service = InMemoryAuthService()
        user_id = service.create_user("newuser@example.com")
        assert isinstance(user_id, str)
        assert service.find_by_email("newuser@example.com") is not None

    def test_initialization_with_users(self):
        """
        Test initializing the service with an existing list of users.
        """

        users = ["user1@example.com", "user2@example.com"]
        service = InMemoryAuthService(users=users)
        assert service.find_by_email(users[0]) is not None
        assert service.find_by_email(users[1]) is not None

    def test_create_user_and_find_it(self):
        """
        Test creating a user and then finding it.
        """

        service = InMemoryAuthService()
        service.create_user("createandfind@example.com")
        found_user = service.find_by_email("createandfind@example.com")
        assert found_user == "createandfind@example.com"
