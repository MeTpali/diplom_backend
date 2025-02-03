from typing import List, Optional
import logging
from fastapi import HTTPException, status

from repositories.locations import LocationRepository
from core.schemas.locations import LocationCreate, LocationUpdate, LocationResponse

logger = logging.getLogger(__name__)

class LocationService:
    def __init__(self, location_repository: LocationRepository):
        self.location_repository = location_repository

    async def get_location_by_id(self, location_id: int) -> LocationResponse:
        location = await self.location_repository.get_location_by_id(location_id)
        if not location:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Location with id {location_id} not found"
            )
        return location

    async def get_all_locations(self) -> List[LocationResponse]:
        return await self.location_repository.get_all_locations()

    async def create_location(self, location_data: LocationCreate) -> LocationResponse:
        # Проверка на отрицательную вместимость
        if location_data.capacity <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Location capacity must be positive"
            )
            
        return await self.location_repository.create_location(location_data)

    async def update_location(self, location_id: int, location_data: LocationUpdate) -> LocationResponse:
        # Проверка существования локации
        await self.get_location_by_id(location_id)
        
        # Проверка на отрицательную вместимость при обновлении
        if location_data.capacity is not None and location_data.capacity <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Location capacity must be positive"
            )

        updated_location = await self.location_repository.update_location(location_id, location_data)
        if not updated_location:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Location with id {location_id} not found"
            )
        return updated_location

    async def delete_location(self, location_id: int) -> bool:
        # Проверка существования локации
        await self.get_location_by_id(location_id)
        return await self.location_repository.delete_location(location_id)

    async def search_locations(self, search_term: str) -> List[LocationResponse]:
        return await self.location_repository.search_locations(search_term)

    async def get_locations_by_capacity(
        self,
        min_capacity: int | None = None,
        max_capacity: int | None = None
    ) -> List[LocationResponse]:
        # Валидация параметров поиска
        if min_capacity is not None and min_capacity < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Minimum capacity cannot be negative"
            )
        if max_capacity is not None and max_capacity < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Maximum capacity cannot be negative"
            )
        if min_capacity is not None and max_capacity is not None and min_capacity > max_capacity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Minimum capacity cannot be greater than maximum capacity"
            )
            
        return await self.location_repository.get_locations_by_capacity(
            min_capacity=min_capacity,
            max_capacity=max_capacity
        )

    async def check_location_availability(self, location_id: int, required_capacity: int) -> bool:
        """
        Проверяет, доступна ли локация для заданной вместимости
        """
        location = await self.get_location_by_id(location_id)
        return location.capacity >= required_capacity 