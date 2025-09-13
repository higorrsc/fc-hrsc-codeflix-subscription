from fastapi import APIRouter, HTTPException

from src.application.exceptions import (
    PlanNotFoundError,
    SubscriptionConflictError,
    UserNotFoundError,
)
from src.application.use_case import SubscribeToPlanInputDTO, SubscribeToPlanOutputDTO
from src.infra.api.dependencies import SubscribeToPlanUseCaseDep

router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])


@router.post("", response_model=SubscribeToPlanOutputDTO, status_code=201)
def create_subscription(
    use_case: SubscribeToPlanUseCaseDep,
    payload: SubscribeToPlanInputDTO,
) -> SubscribeToPlanOutputDTO:
    """
    Route to create a new Subscription.
    """

    try:
        return use_case.execute(payload)
    except (UserNotFoundError, PlanNotFoundError, SubscriptionConflictError) as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
