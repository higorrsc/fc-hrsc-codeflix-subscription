from typing import Optional
from uuid import UUID

from sqlmodel import Session, select

from src.domain.entity import Plan
from src.domain.repository.plan import PlanRepository
from src.infra.db.models import PlanModel


class SQLModelPlanRepository(PlanRepository):
    """
    Class that represents a repository for plans.
    It implements the PlanRepository interface.
    """

    def __init__(self, session: Session):
        """
        Constructor
        """

        self.session = session

    def get_by_id(self, plan_id: UUID) -> Optional[Plan]:
        """
        Get a plan by ID.
        """

        statement = select(PlanModel).where(PlanModel.id == plan_id)
        result = self.session.exec(statement).first()
        return PlanModel.to_entity(result) if result else None

    def get_by_name(self, plan_name: str) -> Optional[Plan]:
        """
        Get a plan by name.
        """

        statement = select(PlanModel).where(PlanModel.name == plan_name)
        result = self.session.exec(statement).first()
        return PlanModel.to_entity(result) if result else None

    def save(self, plan: Plan) -> None:
        """
        Save a plan.
        """

        model = PlanModel.from_entity(plan)
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
