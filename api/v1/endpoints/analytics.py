from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Path, Query
from services.analytic_service import AnalyticService
from core.schemas.analytics import AnalyticCreate, AnalyticUpdate, AnalyticResponse
from api.deps import get_analytic_service

router = APIRouter(
    prefix="/analytics",
    tags=["analytics"],
    responses={404: {"description": "Analytics not found"}}
)

@router.get(
    "/{analytic_id}",
    response_model=AnalyticResponse,
    summary="Get analytics by ID",
    description="Retrieve detailed analytics information by its ID",
    responses={
        200: {"description": "Successfully retrieved analytics"},
        404: {"description": "Analytics with specified ID not found"}
    }
)
async def get_analytic(
    analytic_id: int = Path(..., description="The ID of the analytics to retrieve", gt=0),
    analytic_service: AnalyticService = Depends(get_analytic_service)
):
    """
    Retrieve specific analytics entry by ID with detailed statistics including:
    - Average scores
    - Registration counts
    - Payment statistics
    - Success rates
    """
    return await analytic_service.get_analytic_by_id(analytic_id)

@router.get(
    "/",
    response_model=List[AnalyticResponse],
    summary="Get all analytics",
    description="Retrieve a list of all analytics entries"
)
async def get_analytics(
    analytic_service: AnalyticService = Depends(get_analytic_service)
):
    """
    Get all analytics entries with aggregated statistics for all exams
    """
    return await analytic_service.get_all_analytics()

@router.post(
    "/",
    response_model=AnalyticResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create analytics entry",
    description="Create a new analytics entry with initial data",
    responses={
        201: {"description": "Analytics created successfully"},
        400: {"description": "Invalid input data"}
    }
)
async def create_analytic(
    analytic_data: AnalyticCreate,
    analytic_service: AnalyticService = Depends(get_analytic_service)
):
    """
    Create a new analytics entry with:
    - Exam reference
    - Initial statistics
    - Calculation parameters
    """
    return await analytic_service.create_analytic(analytic_data)

@router.put(
    "/{analytic_id}",
    response_model=AnalyticResponse,
    summary="Update analytics",
    description="Update existing analytics entry with new data",
    responses={
        200: {"description": "Analytics updated successfully"},
        404: {"description": "Analytics not found"},
        400: {"description": "Invalid update data"}
    }
)
async def update_analytic(
    analytic_id: int = Path(..., description="The ID of the analytics to update", gt=0),
    analytic_data: AnalyticUpdate = None,
    analytic_service: AnalyticService = Depends(get_analytic_service)
):
    """
    Update analytics entry with new statistics and calculations
    """
    return await analytic_service.update_analytic(analytic_id, analytic_data)

@router.delete(
    "/{analytic_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete analytics",
    description="Delete analytics entry by ID",
    responses={
        204: {"description": "Analytics successfully deleted"},
        404: {"description": "Analytics not found"}
    }
)
async def delete_analytic(
    analytic_id: int = Path(..., description="The ID of the analytics to delete", gt=0),
    analytic_service: AnalyticService = Depends(get_analytic_service)
):
    """
    Remove analytics entry from the system
    """
    await analytic_service.delete_analytic(analytic_id)

@router.post(
    "/generate/{exam_id}",
    response_model=AnalyticResponse,
    summary="Generate exam analytics",
    description="Generate new analytics for specific exam",
    responses={
        200: {"description": "Analytics generated successfully"},
        404: {"description": "Exam not found"},
        400: {"description": "Unable to generate analytics"}
    }
)
async def generate_exam_analytics(
    exam_id: int = Path(..., description="The ID of the exam to analyze", gt=0),
    analytic_service: AnalyticService = Depends(get_analytic_service)
):
    """
    Generate comprehensive analytics for an exam including:
    - Score distribution
    - Registration statistics
    - Payment analysis
    - Success rates
    - Comparative metrics
    """
    return await analytic_service.generate_exam_analytics(exam_id)

@router.get(
    "/by-score/",
    response_model=List[AnalyticResponse],
    summary="Get analytics by score range",
    description="Filter analytics based on score range"
)
async def get_analytics_by_score_range(
    min_score: Optional[float] = Query(
        None,
        description="Minimum score to filter by",
        ge=0,
        le=100
    ),
    max_score: Optional[float] = Query(
        None,
        description="Maximum score to filter by",
        ge=0,
        le=100
    ),
    analytic_service: AnalyticService = Depends(get_analytic_service)
):
    """
    Retrieve analytics filtered by score range:
    - Optional minimum score
    - Optional maximum score
    - Returns analytics entries within specified range
    """
    return await analytic_service.get_analytics_by_score_range(
        min_score=min_score,
        max_score=max_score
    )

@router.get(
    "/by-registrations/",
    response_model=List[AnalyticResponse],
    summary="Get analytics by registration count",
    description="Filter analytics based on number of registrations"
)
async def get_analytics_by_registration_count(
    min_registrations: Optional[int] = Query(
        None,
        description="Minimum number of registrations",
        ge=0
    ),
    max_registrations: Optional[int] = Query(
        None,
        description="Maximum number of registrations",
        ge=0
    ),
    analytic_service: AnalyticService = Depends(get_analytic_service)
):
    """
    Retrieve analytics filtered by registration count:
    - Optional minimum registration count
    - Optional maximum registration count
    - Useful for analyzing popular/unpopular exams
    """
    return await analytic_service.get_analytics_by_registration_count(
        min_registrations=min_registrations,
        max_registrations=max_registrations
    )

@router.get(
    "/by-payment-ratio/",
    response_model=List[AnalyticResponse],
    summary="Get analytics by payment ratio",
    description="Filter analytics based on payment completion ratio"
)
async def get_analytics_by_payment_ratio(
    min_ratio: Optional[float] = Query(
        None,
        description="Minimum payment ratio (0.0 to 1.0)",
        ge=0,
        le=1
    ),
    analytic_service: AnalyticService = Depends(get_analytic_service)
):
    """
    Retrieve analytics filtered by payment ratio:
    - Ratio represents completed payments / total registrations
    - Optional minimum ratio threshold
    - Useful for financial analysis
    """
    return await analytic_service.get_analytics_by_payment_ratio(min_ratio) 