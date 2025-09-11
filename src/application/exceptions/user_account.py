class UserAlreadyExistsError(Exception):
    """
    Exception raised when trying to create a user that already exists.
    """


class UserNotFoundError(Exception):
    """
    Exception raised when trying to create a user that does not exists.
    """
