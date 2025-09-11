class SubscriptionNotFoundError(Exception):
    """
    Exception raised when trying to cancel a subscription that does not exist.
    """


class SubscriptionAlreadyExistsError(Exception):
    """
    Exception raised when trying to create a subscription that already exists.
    """


class SubscriptionConflictError(Exception):
    """
    Exception raised when trying to create a subscription and the user has one active.
    """
