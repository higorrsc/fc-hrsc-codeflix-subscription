class DuplicatePlanError(Exception):
    """
    Exception raised when trying to create a plan that already exists.
    """


class UserAlreadyExistsError(Exception):
    """
    Exception raised when trying to create a user that already exists.
    """
