from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from src.application.use_case import CreatePlanUseCase, CreateUserAccountUseCase
from src.domain.repository import PlanRepository, UserAccountRepository
from src.infra.auth import AuthService, InMemoryAuthService
from src.infra.db import get_session
from src.infra.db.repository import (
    SQLModelPlanRepository,
    SQLModelUserAccountRepository,
)

SessionDep = Annotated[Session, Depends(get_session)]

### REPOSITORIES ###


def get_plan_repository(session: SessionDep) -> PlanRepository:
    """
    Plan repository dependency.
    """

    return SQLModelPlanRepository(session)


def get_user_account_repository(session: SessionDep) -> UserAccountRepository:
    """
    User Account repository dependency.
    """

    return SQLModelUserAccountRepository(session)


PlanRepositoryDep = Annotated[PlanRepository, Depends(get_plan_repository)]
UserAccountRepositoryDep = Annotated[
    UserAccountRepository, Depends(get_user_account_repository)
]

### EXTERNAL SERVICES ###


def get_auth_service() -> AuthService:
    """
    Auth service dependency.
    """

    # TODO: Replace with actual implementation (Keycloak)
    return InMemoryAuthService()


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]


### USE CASES ###


def get_create_plan_use_case(repository: PlanRepositoryDep) -> CreatePlanUseCase:
    """
    Create plan use case dependency.
    """

    return CreatePlanUseCase(repository)


def get_create_user_account_use_case(
    auth_service: AuthServiceDep,
    repository: UserAccountRepositoryDep,
) -> CreateUserAccountUseCase:
    """
    Create userAccount use case dependency.
    """

    return CreateUserAccountUseCase(auth_service, repository)


CreatePlanUseCaseDep = Annotated[CreatePlanUseCase, Depends(get_create_plan_use_case)]
CreateUserAccountUseCaseDep = Annotated[
    CreateUserAccountUseCase, Depends(get_create_user_account_use_case)
]
