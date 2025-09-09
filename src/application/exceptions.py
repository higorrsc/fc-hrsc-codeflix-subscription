class DuplicatePlanError(Exception):
    """
    Exception raised when trying to create a plan that already exists.
    """


class UserAlreadyExistsError(Exception):
    """
    Exception raised when trying to create a user that already exists.
    """


class SubscriptionNotFoundError(Exception):
    """
    Exception raised when trying to cancel a subscription that does not exist.
    """


class SubscriptionAlreadyExistsError(Exception):
    """
    Exception raised when trying to create a subscription that already exists.
    """
