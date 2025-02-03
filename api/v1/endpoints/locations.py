from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from services.location_service import LocationService
from core.schemas.locations import LocationCreate, LocationUpdate, LocationResponse
from api.deps import get_location_service

router = APIRouter(prefix="/locations", tags=["locations"])

@router.get("/{location_id}", response_model=LocationResponse)
async def get_location(
    location_id: int,
    location_service: LocationService = Depends(get_location_service)
):
    return await location_service.get_location_by_id(location_id)

@router.get("/", response_model=List[LocationResponse])
async def get_locations(
    location_service: LocationService = Depends(get_location_service)
):
    return await location_service.get_all_locations()

@router.post("/", response_model=LocationResponse, status_code=status.HTTP_201_CREATED)
async def create_location(
    location_data: LocationCreate,
    location_service: LocationService = Depends(get_location_service)
):
    return await location_service.create_location(location_data)

@router.put("/{location_id}", response_model=LocationResponse)
async def update_location(
    location_id: int,
    location_data: LocationUpdate,
    location_service: LocationService = Depends(get_location_service)
):
    return await location_service.update_location(location_id, location_data)

@router.delete("/{location_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_location(
    location_id: int,
    location_service: LocationService = Depends(get_location_service)
):
    await location_service.delete_location(location_id)

@router.get("/search/{search_term}", response_model=List[LocationResponse])
async def search_locations(
    search_term: str,
    location_service: LocationService = Depends(get_location_service)
):
    return await location_service.search_locations(search_term)

@router.get("/by-capacity/", response_model=List[LocationResponse])
async def get_locations_by_capacity(
    min_capacity: Optional[int] = None,
    max_capacity: Optional[int] = None,
    location_service: LocationService = Depends(get_location_service)
):
    return await location_service.get_locations_by_capacity(
        min_capacity=min_capacity,
        max_capacity=max_capacity
    )

@router.get("/{location_id}/availability/{required_capacity}")
async def check_location_availability(
    location_id: int,
    required_capacity: int,
    location_service: LocationService = Depends(get_location_service)
):
    return await location_service.check_location_availability(location_id, required_capacity) 