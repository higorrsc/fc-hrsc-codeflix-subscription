from fastapi import APIRouter, HTTPException

from src.application.exceptions.user_account import UserAlreadyExistsError
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
    try:
        return use_case.execute(payload)
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
