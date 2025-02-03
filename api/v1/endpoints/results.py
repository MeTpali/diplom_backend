from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from services.result_service import ResultService
from core.schemas.results import ResultCreate, ResultUpdate, ResultResponse
from api.deps import get_result_service

router = APIRouter(prefix="/results", tags=["results"])

@router.get("/{result_id}", response_model=ResultResponse)
async def get_result(
    result_id: int,
    result_service: ResultService = Depends(get_result_service)
):
    return await result_service.get_result_by_id(result_id)

@router.get("/", response_model=List[ResultResponse])
async def get_results(
    result_service: ResultService = Depends(get_result_service)
):
    return await result_service.get_all_results()

@router.post("/", response_model=ResultResponse, status_code=status.HTTP_201_CREATED)
async def create_result(
    result_data: ResultCreate,
    result_service: ResultService = Depends(get_result_service)
):
    return await result_service.create_result(result_data)

@router.put("/{result_id}", response_model=ResultResponse)
async def update_result(
    result_id: int,
    result_data: ResultUpdate,
    result_service: ResultService = Depends(get_result_service)
):
    return await result_service.update_result(result_id, result_data)

@router.delete("/{result_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_result(
    result_id: int,
    result_service: ResultService = Depends(get_result_service)
):
    await result_service.delete_result(result_id)

@router.get("/user/{user_id}", response_model=List[ResultResponse])
async def get_user_results(
    user_id: int,
    result_service: ResultService = Depends(get_result_service)
):
    return await result_service.get_user_results(user_id)

@router.get("/exam/{exam_id}", response_model=List[ResultResponse])
async def get_exam_results(
    exam_id: int,
    result_service: ResultService = Depends(get_result_service)
):
    return await result_service.get_exam_results(exam_id)

@router.get("/grade/{grade}", response_model=List[ResultResponse])
async def get_results_by_grade(
    grade: str,
    result_service: ResultService = Depends(get_result_service)
):
    return await result_service.get_results_by_grade(grade)

@router.get("/by-score/", response_model=List[ResultResponse])
async def get_results_by_score_range(
    min_score: Optional[float] = None,
    max_score: Optional[float] = None,
    result_service: ResultService = Depends(get_result_service)
):
    return await result_service.get_results_by_score_range(
        min_score=min_score,
        max_score=max_score
    )

@router.get("/calculate-grade/{score}")
async def calculate_grade(
    score: float,
    result_service: ResultService = Depends(get_result_service)
):
    return {"grade": await result_service.calculate_grade(score)} 