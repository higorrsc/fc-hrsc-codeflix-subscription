from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from src.application.exceptions import DuplicatePlanError
from src.domain._shared.value_objects import MonetaryValue
from src.domain.entity import Plan
from src.domain.repository import PlanRepository


class CreatePlanInputDTO(BaseModel):
    """
    Input DTO for creating a plan.
    """

    name: str = Field(min_length=1)
    price: MonetaryValue


class CreatePlanOutputDTO(BaseModel):
    """
    Output DTO for creating a plan.
    """

    id: UUID
    name: str
    price: MonetaryValue
    created_at: datetime
    updated_at: datetime
    is_active: bool


class CreatePlanUseCase:
    """
    Use case for creating a plan.
    """

    def __init__(self, repository: PlanRepository) -> None:
        """
        Initialize the use case.
        """

        self._repository = repository

    def execute(self, input_dto: CreatePlanInputDTO) -> CreatePlanOutputDTO:
        """
        Execute the use case.
        """

        existing_plan = self._repository.get_by_name(input_dto.name)
        if existing_plan:
            raise DuplicatePlanError(
                f"Plan with name '{input_dto.name}' already exists."
            )

        plan = Plan(name=input_dto.name, price=input_dto.price)
        self._repository.save(plan)

        return CreatePlanOutputDTO(
            id=plan.id,
            name=plan.name,
            price=plan.price,
            created_at=plan.created_at,
            updated_at=plan.updated_at,
            is_active=plan.is_active,
        )
