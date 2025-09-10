from typing import List, Optional
from uuid import UUID

from src.domain.plan import Plan


class InMemoryPlanRepository:
    """
    In-memory repository for managing plans.
    """

    def __init__(self, plans: Optional[List[Plan]] = None) -> None:
        """
        Initialize the repository with an optional list of plans.
        """

        self.plans = plans or []

    def find_by_name(self, name: str) -> Optional[Plan]:
        """
        Find a plan by its name.
        """

        for plan in self.plans:
            if plan.name == name:
                return plan

        return None

    def save(self, plan: Plan) -> None:
        """
        Save a plan.
        """

        if self.find_by_name(plan.name):
            raise ValueError(f"Plan with name '{plan.name}' already exists.")

        self.plans.append(plan)

    def get_by_id(self, plan_id: UUID):
        """
        Get a plan by its ID.
        """

        for plan in self.plans:
            if plan.id == plan_id:
                return plan

        return None
