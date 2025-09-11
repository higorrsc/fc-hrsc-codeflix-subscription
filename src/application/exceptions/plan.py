class DuplicatePlanError(Exception):
    """
    Exception raised when trying to create a plan that already exists.
    """


class PlanNotFoundError(Exception):
    """
    Exception raised when trying to find a plan that does not exist.
    """
