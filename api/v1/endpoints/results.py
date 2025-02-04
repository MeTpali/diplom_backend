from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Path, Query
from services.result_service import ResultService
from core.schemas.results import ResultCreate, ResultUpdate, ResultResponse
from api.deps import get_result_service

router = APIRouter(
    prefix="/results",
    tags=["results"],
    responses={404: {"description": "Result not found"}}
)

@router.get(
    "/{result_id}",
    response_model=ResultResponse,
    summary="Get result by ID",
    description="Retrieve detailed information about a specific exam result",
    responses={
        200: {"description": "Successfully retrieved result details"},
        404: {"description": "Result not found"}
    }
)
async def get_result(
    result_id: int = Path(..., description="The ID of the result to retrieve", gt=0),
    result_service: ResultService = Depends(get_result_service)
):
    """
    Get detailed information about a specific exam result, including:
    - Score and grade
    - User information
    - Exam details
    - Comments and feedback
    """
    return await result_service.get_result_by_id(result_id)

@router.get(
    "/",
    response_model=List[ResultResponse],
    summary="Get all results",
    description="Retrieve a list of all exam results"
)
async def get_results(
    result_service: ResultService = Depends(get_result_service)
):
    """
    Get a list of all exam results:
    - Sorted by date (newest first)
    - Including grades and scores
    - With user and exam details
    """
    return await result_service.get_all_results()

@router.post(
    "/",
    response_model=ResultResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create new result",
    description="Record a new exam result",
    responses={
        201: {"description": "Result created successfully"},
        400: {"description": "Invalid result data"},
        404: {"description": "User or exam not found"}
    }
)
async def create_result(
    result_data: ResultCreate,
    result_service: ResultService = Depends(get_result_service)
):
    """
    Create a new exam result with validation:
    - Verify exam completion
    - Calculate grade from score
    - Record feedback and comments
    - Link to user and exam
    """
    return await result_service.create_result(result_data)

@router.put(
    "/{result_id}",
    response_model=ResultResponse,
    summary="Update result",
    description="Update an existing exam result",
    responses={
        200: {"description": "Result updated successfully"},
        404: {"description": "Result not found"},
        400: {"description": "Invalid update data"}
    }
)
async def update_result(
    result_id: int = Path(..., description="The ID of the result to update", gt=0),
    result_data: ResultUpdate = None,
    result_service: ResultService = Depends(get_result_service)
):
    """
    Update result information:
    - Modify score or grade
    - Update comments
    - Add additional feedback
    """
    return await result_service.update_result(result_id, result_data)

@router.delete(
    "/{result_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete result",
    description="Delete an exam result",
    responses={
        204: {"description": "Result successfully deleted"},
        404: {"description": "Result not found"}
    }
)
async def delete_result(
    result_id: int = Path(..., description="The ID of the result to delete", gt=0),
    result_service: ResultService = Depends(get_result_service)
):
    """
    Delete a result record:
    - Removes all associated data
    - Cannot be undone
    """
    await result_service.delete_result(result_id)

@router.get(
    "/user/{user_id}",
    response_model=List[ResultResponse],
    summary="Get user results",
    description="Retrieve all results for a specific user"
)
async def get_user_results(
    user_id: int = Path(..., description="The ID of the user", gt=0),
    result_service: ResultService = Depends(get_result_service)
):
    """
    Get all results for a specific user:
    - Includes all exams taken
    - Sorted by date
    - With grades and scores
    """
    return await result_service.get_user_results(user_id)

@router.get(
    "/exam/{exam_id}",
    response_model=List[ResultResponse],
    summary="Get exam results",
    description="Retrieve all results for a specific exam"
)
async def get_exam_results(
    exam_id: int = Path(..., description="The ID of the exam", gt=0),
    result_service: ResultService = Depends(get_result_service)
):
    """
    Get all results for a specific exam:
    - Shows score distribution
    - Includes all grades
    - With user details
    """
    return await result_service.get_exam_results(exam_id)

@router.get(
    "/grade/{grade}",
    response_model=List[ResultResponse],
    summary="Get results by grade",
    description="Filter results by specific grade"
)
async def get_results_by_grade(
    grade: str = Path(..., description="The grade to filter by (e.g., A, B, C, D, F)"),
    result_service: ResultService = Depends(get_result_service)
):
    """
    Get results filtered by grade:
    - Specific grade results
    - Sorted by score
    - With exam and user details
    """
    return await result_service.get_results_by_grade(grade)

@router.get(
    "/by-score/",
    response_model=List[ResultResponse],
    summary="Get results by score range",
    description="Filter results based on score range"
)
async def get_results_by_score_range(
    min_score: Optional[float] = Query(None, description="Minimum score", ge=0, le=100),
    max_score: Optional[float] = Query(None, description="Maximum score", ge=0, le=100),
    result_service: ResultService = Depends(get_result_service)
):
    """
    Find results within score range:
    - Optional minimum score
    - Optional maximum score
    - Sorted by score
    - With grade information
    """
    return await result_service.get_results_by_score_range(
        min_score=min_score,
        max_score=max_score
    )

@router.get(
    "/calculate-grade/{score}",
    summary="Calculate grade from score",
    description="Convert a numerical score to a letter grade",
    responses={
        200: {
            "description": "Grade calculation successful",
            "content": {
                "application/json": {
                    "example": {
                        "grade": "A"
                    }
                }
            }
        },
        400: {"description": "Invalid score"}
    }
)
async def calculate_grade(
    score: float = Path(..., description="The score to convert to grade", ge=0, le=100),
    result_service: ResultService = Depends(get_result_service)
):
    """
    Calculate letter grade from numerical score:
    - Score must be between 0 and 100
    - Returns corresponding letter grade
    - Based on grading scale
    """
    return {"grade": await result_service.calculate_grade(score)} 