from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from src.domain.entity import Plan


class PlanRepository(ABC):
    """
    Abstract class for Plan Repository.
    """

    @abstractmethod
    def get_by_id(self, plan_id: UUID) -> Optional[Plan]:
        """
        Get a plan by ID
        """

        raise NotImplementedError

    @abstractmethod
    def get_by_name(self, plan_name: str) -> Optional[Plan]:
        """
        Get a plan by name
        """

        raise NotImplementedError

    @abstractmethod
    def save(self, plan: Plan) -> None:
        """
        Save an Plan
        """

        raise NotImplementedError
