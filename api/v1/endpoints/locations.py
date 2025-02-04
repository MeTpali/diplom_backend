from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Path, Query
from services.location_service import LocationService
from core.schemas.locations import LocationCreate, LocationUpdate, LocationResponse
from api.deps import get_location_service

router = APIRouter(
    prefix="/locations",
    tags=["locations"],
    responses={404: {"description": "Location not found"}}
)

@router.get(
    "/{location_id}",
    response_model=LocationResponse,
    summary="Get location by ID",
    description="Retrieve detailed information about a specific location",
    responses={
        200: {"description": "Successfully retrieved location details"},
        404: {"description": "Location not found"}
    }
)
async def get_location(
    location_id: int = Path(..., description="The ID of the location to retrieve", gt=0),
    location_service: LocationService = Depends(get_location_service)
):
    """
    Get detailed information about a specific location, including:
    - Basic location details
    - Current capacity
    - Address information
    - Scheduled exams count
    """
    return await location_service.get_location_by_id(location_id)

@router.get(
    "/",
    response_model=List[LocationResponse],
    summary="Get all locations",
    description="Retrieve a list of all available exam locations"
)
async def get_locations(
    location_service: LocationService = Depends(get_location_service)
):
    """
    Get a list of all exam locations:
    - Sorted by name
    - Including capacity information
    - With current availability status
    """
    return await location_service.get_all_locations()

@router.post(
    "/",
    response_model=LocationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create new location",
    description="Create a new exam location with all necessary details",
    responses={
        201: {"description": "Location created successfully"},
        400: {"description": "Invalid input data"}
    }
)
async def create_location(
    location_data: LocationCreate,
    location_service: LocationService = Depends(get_location_service)
):
    """
    Create a new exam location with validation:
    - Name must be unique
    - Capacity must be positive
    - Valid address required
    - Optional description and facilities
    """
    return await location_service.create_location(location_data)

@router.put(
    "/{location_id}",
    response_model=LocationResponse,
    summary="Update location",
    description="Update an existing location's details",
    responses={
        200: {"description": "Location updated successfully"},
        404: {"description": "Location not found"},
        400: {"description": "Invalid update data"}
    }
)
async def update_location(
    location_id: int = Path(..., description="The ID of the location to update", gt=0),
    location_data: LocationUpdate = None,
    location_service: LocationService = Depends(get_location_service)
):
    """
    Update location details with validation:
    - Cannot reduce capacity below current exam bookings
    - Name must remain unique
    - Address updates must be valid
    """
    return await location_service.update_location(location_id, location_data)

@router.delete(
    "/{location_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete location",
    description="Delete a location by ID",
    responses={
        204: {"description": "Location successfully deleted"},
        404: {"description": "Location not found"},
        400: {"description": "Cannot delete location with scheduled exams"}
    }
)
async def delete_location(
    location_id: int = Path(..., description="The ID of the location to delete", gt=0),
    location_service: LocationService = Depends(get_location_service)
):
    """
    Delete a location if:
    - Location exists
    - Has no scheduled exams
    - Has no active bookings
    """
    await location_service.delete_location(location_id)

@router.get(
    "/search/{search_term}",
    response_model=List[LocationResponse],
    summary="Search locations",
    description="Search locations by name or address"
)
async def search_locations(
    search_term: str = Path(..., description="The search term to look for", min_length=2),
    location_service: LocationService = Depends(get_location_service)
):
    """
    Search locations by keyword:
    - Searches in name and address
    - Case-insensitive
    - Partial matches supported
    - Returns sorted by relevance
    """
    return await location_service.search_locations(search_term)

@router.get(
    "/by-capacity/",
    response_model=List[LocationResponse],
    summary="Get locations by capacity",
    description="Find locations based on their capacity range"
)
async def get_locations_by_capacity(
    min_capacity: Optional[int] = Query(
        None,
        description="Minimum capacity required",
        ge=0
    ),
    max_capacity: Optional[int] = Query(
        None,
        description="Maximum capacity limit",
        ge=0
    ),
    location_service: LocationService = Depends(get_location_service)
):
    """
    Find locations by capacity range:
    - Optional minimum capacity
    - Optional maximum capacity
    - Returns sorted by capacity
    - Includes availability status
    """
    return await location_service.get_locations_by_capacity(
        min_capacity=min_capacity,
        max_capacity=max_capacity
    )

@router.get(
    "/{location_id}/availability/{required_capacity}",
    summary="Check location availability",
    description="Check if a location can accommodate a specific capacity",
    responses={
        200: {
            "description": "Availability check successful",
            "content": {
                "application/json": {
                    "example": {
                        "available": True,
                        "remaining_capacity": 50,
                        "has_conflicts": False
                    }
                }
            }
        },
        404: {"description": "Location not found"}
    }
)
async def check_location_availability(
    location_id: int = Path(..., description="The ID of the location to check", gt=0),
    required_capacity: int = Path(..., description="The required capacity to check for", gt=0),
    location_service: LocationService = Depends(get_location_service)
):
    """
    Check location availability:
    - Verifies total capacity
    - Checks existing bookings
    - Considers scheduled exams
    - Returns detailed availability status
    """
    return await location_service.check_location_availability(location_id, required_capacity) 