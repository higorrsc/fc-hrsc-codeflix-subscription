from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from src.application.use_case.create_plan import CreatePlanUseCase
from src.domain.repository import PlanRepository
from src.infra.db import get_session
from src.infra.db.repository import SQLModelPlanRepository

SessionDep = Annotated[Session, Depends(get_session)]


def get_plan_repository(session: SessionDep) -> PlanRepository:
    """
    Plan repository dependency.
    """

    return SQLModelPlanRepository(session)


PlanRepositoryDep = Annotated[PlanRepository, Depends(get_plan_repository)]


def get_create_plan_use_case(repository: PlanRepositoryDep) -> CreatePlanUseCase:
    """
    Create plan use case dependency.
    """

    return CreatePlanUseCase(repository)


CreatePlanUseCaseDep = Annotated[CreatePlanUseCase, Depends(get_create_plan_use_case)]
