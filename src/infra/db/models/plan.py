from datetime import datetime
from decimal import Decimal
from uuid import UUID

from sqlmodel import Field, SQLModel

from src.domain._shared import Currency, MonetaryValue
from src.domain.entity import Plan


class PlanModel(SQLModel, table=True):
    """
    Defines a model that represents a plan
    """

    __tablename__ = "plans"  # type: ignore

    id: UUID = Field(primary_key=True)
    name: str = Field(index=True, unique=True)
    price_amount: Decimal = Field()
    price_currency: str = Field()
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    is_active: bool = Field(default=True)

    @classmethod
    def from_entity(cls, plan: Plan) -> "PlanModel":
        """
        Transform a Plan Entity in a Plan Model
        """

        return cls(
            id=plan.id,
            name=plan.name,
            price_amount=plan.price.amount,
            price_currency=plan.price.currency,
            created_at=plan.created_at,
            updated_at=plan.updated_at,
            is_active=plan.is_active,
        )

    @classmethod
    def to_entity(cls, plan_model: "PlanModel") -> Plan:
        """
        Transform a Plan Model in a Plan Entity
        """

        return Plan(
            id=plan_model.id,
            name=plan_model.name,
            price=MonetaryValue(
                amount=plan_model.price_amount,
                currency=Currency(plan_model.price_currency),
            ),
            created_at=plan_model.created_at,
            updated_at=plan_model.updated_at,
            is_active=plan_model.is_active,
        )
