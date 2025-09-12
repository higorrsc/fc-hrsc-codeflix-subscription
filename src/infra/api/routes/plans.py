from fastapi import APIRouter, HTTPException

from src.application.exceptions.plan import DuplicatePlanError
from src.application.use_case.create_plan import CreatePlanInputDTO, CreatePlanOutputDTO
from src.infra.api.dependencies import CreatePlanUseCaseDep

router = APIRouter(prefix="/plans", tags=["plans"])


@router.post("", response_model=CreatePlanOutputDTO, status_code=201)
def create_plan(
    use_case: CreatePlanUseCaseDep,
    payload: CreatePlanInputDTO,
) -> CreatePlanOutputDTO:
    """
    Route to create a new plan.
    """

    try:
        return use_case.execute(payload)
    except DuplicatePlanError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
