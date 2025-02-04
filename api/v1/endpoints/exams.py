from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Path, Query
from services.exam_service import ExamService
from core.schemas.exams import ExamCreate, ExamUpdate, ExamResponse
from api.deps import get_exam_service

router = APIRouter(
    prefix="/exams",
    tags=["exams"],
    responses={404: {"description": "Exam not found"}}
)

@router.get(
    "/{exam_id}",
    response_model=ExamResponse,
    summary="Get exam by ID",
    description="Retrieve detailed information about a specific exam",
    responses={
        200: {"description": "Successfully retrieved exam details"},
        404: {"description": "Exam not found"}
    }
)
async def get_exam(
    exam_id: int = Path(..., description="The ID of the exam to retrieve", gt=0),
    exam_service: ExamService = Depends(get_exam_service)
):
    """
    Get detailed information about a specific exam, including:
    - Basic exam details
    - Location information
    - Current registration count
    - Status and availability
    """
    return await exam_service.get_exam_by_id(exam_id)

@router.get(
    "/",
    response_model=List[ExamResponse],
    summary="Get all exams",
    description="Retrieve a list of all available exams"
)
async def get_exams(
    exam_service: ExamService = Depends(get_exam_service)
):
    """
    Get a list of all exams in the system:
    - Sorted by date (newest first)
    - Including basic exam information
    - With current registration status
    """
    return await exam_service.get_all_exams()

@router.post(
    "/",
    response_model=ExamResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create new exam",
    description="Create a new exam with all necessary details",
    responses={
        201: {"description": "Exam created successfully"},
        400: {"description": "Invalid input data"},
        404: {"description": "Referenced location not found"}
    }
)
async def create_exam(
    exam_data: ExamCreate,
    exam_service: ExamService = Depends(get_exam_service)
):
    """
    Create a new exam with validation:
    - Date must be in the future
    - Capacity must not exceed location capacity
    - Price must be positive
    - Location must exist and be available
    """
    return await exam_service.create_exam(exam_data)

@router.put(
    "/{exam_id}",
    response_model=ExamResponse,
    summary="Update exam",
    description="Update an existing exam's details",
    responses={
        200: {"description": "Exam updated successfully"},
        404: {"description": "Exam not found"},
        400: {"description": "Invalid update data"}
    }
)
async def update_exam(
    exam_id: int = Path(..., description="The ID of the exam to update", gt=0),
    exam_data: ExamUpdate = None,
    exam_service: ExamService = Depends(get_exam_service)
):
    """
    Update exam details with validation:
    - Cannot update if exam has started
    - Cannot reduce capacity below current registrations
    - Date changes must be in the future
    """
    return await exam_service.update_exam(exam_id, exam_data)

@router.delete(
    "/{exam_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete exam",
    description="Delete an exam by ID",
    responses={
        204: {"description": "Exam successfully deleted"},
        404: {"description": "Exam not found"},
        400: {"description": "Cannot delete exam with existing registrations"}
    }
)
async def delete_exam(
    exam_id: int = Path(..., description="The ID of the exam to delete", gt=0),
    exam_service: ExamService = Depends(get_exam_service)
):
    """
    Delete an exam if:
    - Exam exists
    - Has no active registrations
    - Has not started yet
    """
    await exam_service.delete_exam(exam_id)

@router.get(
    "/subject/{subject}",
    response_model=List[ExamResponse],
    summary="Get exams by subject",
    description="Find all exams for a specific subject"
)
async def get_exams_by_subject(
    subject: str = Path(..., description="The subject to search for", min_length=2),
    exam_service: ExamService = Depends(get_exam_service)
):
    """
    Find exams by subject:
    - Case-insensitive search
    - Partial matches supported
    - Sorted by date
    """
    return await exam_service.get_exams_by_subject(subject)

@router.get(
    "/organizer/{organizer_id}",
    response_model=List[ExamResponse],
    summary="Get exams by organizer",
    description="Find all exams created by a specific organizer"
)
async def get_exams_by_organizer(
    organizer_id: int = Path(..., description="The ID of the organizer", gt=0),
    exam_service: ExamService = Depends(get_exam_service)
):
    """
    Get all exams associated with a specific organizer:
    - Includes both active and past exams
    - Sorted by date
    """
    return await exam_service.get_exams_by_organizer(organizer_id)

@router.get(
    "/location/{location_id}",
    response_model=List[ExamResponse],
    summary="Get exams by location",
    description="Find all exams scheduled at a specific location"
)
async def get_exams_by_location(
    location_id: int = Path(..., description="The ID of the location", gt=0),
    exam_service: ExamService = Depends(get_exam_service)
):
    """
    Get exams at a specific location:
    - Includes upcoming and past exams
    - Sorted by date
    - With availability information
    """
    return await exam_service.get_exams_by_location(location_id)

@router.get(
    "/upcoming/",
    response_model=List[ExamResponse],
    summary="Get upcoming exams",
    description="Get all future exams that haven't started yet"
)
async def get_upcoming_exams(
    exam_service: ExamService = Depends(get_exam_service)
):
    """
    Get all upcoming exams:
    - Only future dates
    - Only active status
    - Sorted by nearest date first
    - Including registration availability
    """
    return await exam_service.get_upcoming_exams()

@router.get(
    "/search/{search_term}",
    response_model=List[ExamResponse],
    summary="Search exams",
    description="Search exams by keyword in subject or description"
)
async def search_exams(
    search_term: str = Path(..., description="The search term to look for", min_length=2),
    exam_service: ExamService = Depends(get_exam_service)
):
    """
    Search exams by keyword:
    - Searches in subject and description
    - Case-insensitive
    - Partial matches supported
    - Returns sorted by relevance
    """
    return await exam_service.search_exams(search_term)

@router.get(
    "/{exam_id}/availability",
    summary="Check exam availability",
    description="Check if an exam is available for registration",
    responses={
        200: {
            "description": "Availability check successful",
            "content": {
                "application/json": {
                    "example": {
                        "available": True,
                        "remaining_spots": 10,
                        "registration_open": True
                    }
                }
            }
        },
        404: {"description": "Exam not found"}
    }
)
async def check_exam_availability(
    exam_id: int = Path(..., description="The ID of the exam to check", gt=0),
    exam_service: ExamService = Depends(get_exam_service)
):
    """
    Check exam availability:
    - Verifies if exam date is in future
    - Checks remaining capacity
    - Confirms exam is active
    - Returns detailed availability status
    """
    return await exam_service.check_exam_availability(exam_id) 