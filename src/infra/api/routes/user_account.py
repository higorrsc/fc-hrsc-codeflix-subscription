from fastapi import APIRouter

from src.application.use_case import (
    CreateUserAccountInputDTO,
    CreateUserAccountOutputDTO,
)
from src.infra.api.dependencies import CreateUserAccountUseCaseDep

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.post("", response_model=CreateUserAccountOutputDTO, status_code=201)
def create_user_account(
    use_case: CreateUserAccountUseCaseDep,
    payload: CreateUserAccountInputDTO,
) -> CreateUserAccountOutputDTO:
    """
    Route to create a new userAccount.
    """

    return use_case.execute(payload)
