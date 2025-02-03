from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from services.analytic_service import AnalyticService
from core.schemas.analytics import AnalyticCreate, AnalyticUpdate, AnalyticResponse
from api.deps import get_analytic_service

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/{analytic_id}", response_model=AnalyticResponse)
async def get_analytic(
    analytic_id: int,
    analytic_service: AnalyticService = Depends(get_analytic_service)
):
    return await analytic_service.get_analytic_by_id(analytic_id)

@router.get("/", response_model=List[AnalyticResponse])
async def get_analytics(
    analytic_service: AnalyticService = Depends(get_analytic_service)
):
    return await analytic_service.get_all_analytics()

@router.post("/", response_model=AnalyticResponse, status_code=status.HTTP_201_CREATED)
async def create_analytic(
    analytic_data: AnalyticCreate,
    analytic_service: AnalyticService = Depends(get_analytic_service)
):
    return await analytic_service.create_analytic(analytic_data)

@router.put("/{analytic_id}", response_model=AnalyticResponse)
async def update_analytic(
    analytic_id: int,
    analytic_data: AnalyticUpdate,
    analytic_service: AnalyticService = Depends(get_analytic_service)
):
    return await analytic_service.update_analytic(analytic_id, analytic_data)

@router.delete("/{analytic_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_analytic(
    analytic_id: int,
    analytic_service: AnalyticService = Depends(get_analytic_service)
):
    await analytic_service.delete_analytic(analytic_id)

@router.post("/generate/{exam_id}", response_model=AnalyticResponse)
async def generate_exam_analytics(
    exam_id: int,
    analytic_service: AnalyticService = Depends(get_analytic_service)
):
    return await analytic_service.generate_exam_analytics(exam_id)

@router.get("/by-score/", response_model=List[AnalyticResponse])
async def get_analytics_by_score_range(
    min_score: Optional[float] = None,
    max_score: Optional[float] = None,
    analytic_service: AnalyticService = Depends(get_analytic_service)
):
    return await analytic_service.get_analytics_by_score_range(
        min_score=min_score,
        max_score=max_score
    )

@router.get("/by-registrations/", response_model=List[AnalyticResponse])
async def get_analytics_by_registration_count(
    min_registrations: Optional[int] = None,
    max_registrations: Optional[int] = None,
    analytic_service: AnalyticService = Depends(get_analytic_service)
):
    return await analytic_service.get_analytics_by_registration_count(
        min_registrations=min_registrations,
        max_registrations=max_registrations
    )

@router.get("/by-payment-ratio/", response_model=List[AnalyticResponse])
async def get_analytics_by_payment_ratio(
    min_ratio: Optional[float] = None,
    analytic_service: AnalyticService = Depends(get_analytic_service)
):
    return await analytic_service.get_analytics_by_payment_ratio(min_ratio) 