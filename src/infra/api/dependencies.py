from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from src.application.use_case import CreatePlanUseCase, CreateUserAccountUseCase
from src.application.use_case.subscribe_to_plan import SubscribeToPlanUseCase
from src.domain.repository import (
    PlanRepository,
    SubscriptionRepository,
    UserAccountRepository,
)
from src.infra.auth import AuthService, InMemoryAuthService
from src.infra.db import get_session
from src.infra.db.repository import (
    SQLModelPlanRepository,
    SQLModelSubscriptionRepository,
    SQLModelUserAccountRepository,
)
from src.infra.notification import ConsoleNotificationService, NotificationService
from src.infra.payment import FakePaymentGateway, PaymentGateway

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


def get_subscription_repository(session: SessionDep) -> SubscriptionRepository:
    """
    Subscription repository dependency.
    """

    return SQLModelSubscriptionRepository(session)


PlanRepositoryDep = Annotated[
    PlanRepository,
    Depends(get_plan_repository),
]
UserAccountRepositoryDep = Annotated[
    UserAccountRepository,
    Depends(get_user_account_repository),
]
SubscriptionRepositoryDep = Annotated[
    SubscriptionRepository,
    Depends(get_subscription_repository),
]

### EXTERNAL SERVICES ###


def get_auth_service() -> AuthService:
    """
    Auth service dependency.
    """

    # TODO: Replace with actual implementation (Keycloak)
    return InMemoryAuthService()


def get_payment_gateway() -> PaymentGateway:
    """
    Payment gateway dependency.
    """

    # TODO: Replace with actual implementation (Stripe)
    return FakePaymentGateway()


def get_notification_service() -> NotificationService:
    """
    Notification service dependency.
    """

    # TODO: Replace with actual implementation (Email)
    return ConsoleNotificationService()


AuthServiceDep = Annotated[
    AuthService,
    Depends(get_auth_service),
]
PaymentGatewayDep = Annotated[
    PaymentGateway,
    Depends(get_payment_gateway),
]
NotificationServiceDep = Annotated[
    NotificationService,
    Depends(get_notification_service),
]

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


def get_subscribe_to_plan_use_case(
    subscription_repository: SubscriptionRepositoryDep,
    user_repository: UserAccountRepositoryDep,
    plan_repository: PlanRepositoryDep,
    payment_gateway: PaymentGatewayDep,
    notification_service: NotificationServiceDep,
) -> SubscribeToPlanUseCase:
    """
    Subscribe to plan use case dependency.
    """

    return SubscribeToPlanUseCase(
        subscription_repository=subscription_repository,
        user_repository=user_repository,
        plan_repository=plan_repository,
        payment_gateway=payment_gateway,
        notification_service=notification_service,
    )


CreatePlanUseCaseDep = Annotated[
    CreatePlanUseCase,
    Depends(get_create_plan_use_case),
]
CreateUserAccountUseCaseDep = Annotated[
    CreateUserAccountUseCase, Depends(get_create_user_account_use_case)
]
SubscribeToPlanUseCaseDep = Annotated[
    SubscribeToPlanUseCase,
    Depends(get_subscribe_to_plan_use_case),
]
