class DuplicatePlanError(Exception):
    """
    Exception raised when trying to create a plan that already exists.
    """


class PlanNotFoundError(Exception):
    """
    Exception raised when trying to find a plan that does not exist.
    """


class UserAlreadyExistsError(Exception):
    """
    Exception raised when trying to create a user that already exists.
    """


class UserDoesNotExistsError(Exception):
    """
    Exception raised when trying to create a user that does not exists.
    """


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
