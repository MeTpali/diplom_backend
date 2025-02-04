from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Path, Query
from services.registration_service import RegistrationService
from core.schemas.registrations import RegistrationCreate, RegistrationUpdate, RegistrationResponse
from api.deps import get_registration_service

router = APIRouter(
    prefix="/registrations",
    tags=["registrations"],
    responses={404: {"description": "Registration not found"}}
)

@router.get(
    "/{registration_id}",
    response_model=RegistrationResponse,
    summary="Get registration by ID",
    description="Retrieve detailed information about a specific exam registration",
    responses={
        200: {"description": "Successfully retrieved registration details"},
        404: {"description": "Registration not found"}
    }
)
async def get_registration(
    registration_id: int = Path(..., description="The ID of the registration to retrieve", gt=0),
    registration_service: RegistrationService = Depends(get_registration_service)
):
    """
    Get detailed information about a specific registration, including:
    - Registration status
    - Payment status
    - User details
    - Exam information
    """
    return await registration_service.get_registration_by_id(registration_id)

@router.get(
    "/",
    response_model=List[RegistrationResponse],
    summary="Get all registrations",
    description="Retrieve a list of all exam registrations"
)
async def get_registrations(
    registration_service: RegistrationService = Depends(get_registration_service)
):
    """
    Get a list of all registrations:
    - Sorted by date (newest first)
    - Including status information
    - With user and exam details
    """
    return await registration_service.get_all_registrations()

@router.post(
    "/",
    response_model=RegistrationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create new registration",
    description="Register a user for an exam",
    responses={
        201: {"description": "Registration created successfully"},
        400: {"description": "Invalid registration data"},
        404: {"description": "User or exam not found"}
    }
)
async def create_registration(
    registration_data: RegistrationCreate,
    registration_service: RegistrationService = Depends(get_registration_service)
):
    """
    Create a new exam registration with validation:
    - Verify exam availability
    - Check user eligibility
    - Validate registration period
    - Initialize payment status
    """
    return await registration_service.create_registration(registration_data)

@router.put(
    "/{registration_id}",
    response_model=RegistrationResponse,
    summary="Update registration",
    description="Update registration details or status",
    responses={
        200: {"description": "Registration updated successfully"},
        404: {"description": "Registration not found"},
        400: {"description": "Invalid update data"}
    }
)
async def update_registration(
    registration_id: int = Path(..., description="The ID of the registration to update", gt=0),
    registration_data: RegistrationUpdate = None,
    registration_service: RegistrationService = Depends(get_registration_service)
):
    """
    Update registration information:
    - Modify registration status
    - Update payment status
    - Change exam details (if allowed)
    """
    return await registration_service.update_registration(registration_id, registration_data)

@router.delete(
    "/{registration_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete registration",
    description="Cancel and delete an exam registration",
    responses={
        204: {"description": "Registration successfully deleted"},
        404: {"description": "Registration not found"},
        400: {"description": "Cannot delete active registration"}
    }
)
async def delete_registration(
    registration_id: int = Path(..., description="The ID of the registration to delete", gt=0),
    registration_service: RegistrationService = Depends(get_registration_service)
):
    """
    Delete a registration if:
    - Registration exists
    - Exam hasn't started
    - Payment hasn't been processed
    """
    await registration_service.delete_registration(registration_id)

@router.get(
    "/user/{user_id}",
    response_model=List[RegistrationResponse],
    summary="Get user registrations",
    description="Retrieve all registrations for a specific user"
)
async def get_user_registrations(
    user_id: int = Path(..., description="The ID of the user", gt=0),
    registration_service: RegistrationService = Depends(get_registration_service)
):
    """
    Get all registrations for a specific user:
    - Includes all registration statuses
    - Sorted by exam date
    - With payment information
    """
    return await registration_service.get_user_registrations(user_id)

@router.get(
    "/exam/{exam_id}",
    response_model=List[RegistrationResponse],
    summary="Get exam registrations",
    description="Retrieve all registrations for a specific exam"
)
async def get_exam_registrations(
    exam_id: int = Path(..., description="The ID of the exam", gt=0),
    registration_service: RegistrationService = Depends(get_registration_service)
):
    """
    Get all registrations for a specific exam:
    - Shows registration distribution
    - Includes payment statuses
    - With user details
    """
    return await registration_service.get_exam_registrations(exam_id)

@router.get(
    "/status/{status}",
    response_model=List[RegistrationResponse],
    summary="Get registrations by status",
    description="Filter registrations by their current status"
)
async def get_registrations_by_status(
    status: str = Path(..., description="Registration status (e.g., pending, confirmed, cancelled)"),
    registration_service: RegistrationService = Depends(get_registration_service)
):
    """
    Get registrations filtered by status:
    - Supports multiple status types
    - Sorted by date
    - With full registration details
    """
    return await registration_service.get_registrations_by_status(status)

@router.get(
    "/payment-status/{payment_status}",
    response_model=List[RegistrationResponse],
    summary="Get registrations by payment status",
    description="Filter registrations based on their payment status"
)
async def get_registrations_by_payment_status(
    payment_status: str = Path(..., description="Payment status (e.g., pending, paid, refunded)"),
    registration_service: RegistrationService = Depends(get_registration_service)
):
    """
    Get registrations filtered by payment status:
    - Shows payment progress
    - Includes registration details
    - Sorted by payment date
    """
    return await registration_service.get_registrations_by_payment_status(payment_status)

@router.get(
    "/check-availability/",
    summary="Check registration availability",
    description="Check if a user can register for a specific exam",
    responses={
        200: {
            "description": "Availability check successful",
            "content": {
                "application/json": {
                    "example": {
                        "available": True,
                        "reason": "Registration is available",
                        "remaining_spots": 10
                    }
                }
            }
        },
        404: {"description": "User or exam not found"}
    }
)
async def check_registration_availability(
    user_id: int = Query(..., description="The ID of the user", gt=0),
    exam_id: int = Query(..., description="The ID of the exam", gt=0),
    registration_service: RegistrationService = Depends(get_registration_service)
):
    """
    Check if registration is possible:
    - Verifies exam capacity
    - Checks user eligibility
    - Validates registration period
    - Returns availability status
    """
    return await registration_service.check_registration_availability(user_id, exam_id) 