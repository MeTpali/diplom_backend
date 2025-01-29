from typing import List, Optional
import logging
from sqlalchemy import select, or_, delete
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.locations import Location
from core.schemas.locations import LocationCreate, LocationUpdate, LocationResponse

logger = logging.getLogger(__name__)

class LocationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    def _model_to_schema(self, location: Location) -> LocationResponse:
        return LocationResponse.model_validate(location)

    async def get_location_by_id(self, location_id: int) -> Optional[LocationResponse]:
        logger.info(f"Getting location by id: {location_id}")
        query = select(Location).where(Location.id == location_id)
        result = await self.session.execute(query)
        location = result.scalar_one_or_none()
        if location is None:
            logger.warning(f"Location with id {location_id} not found")
        return self._model_to_schema(location) if location else None

    async def get_all_locations(self) -> List[LocationResponse]:
        logger.info("Getting all locations")
        query = select(Location)
        result = await self.session.execute(query)
        locations = result.scalars().all()
        return [self._model_to_schema(location) for location in locations]

    async def create_location(self, location_data: LocationCreate) -> LocationResponse:
        logger.info(f"Creating new location with name: {location_data.name}")
        location = Location(**location_data.model_dump())
        self.session.add(location)
        await self.session.commit()
        await self.session.refresh(location)
        logger.info(f"Successfully created location with id: {location.id}")
        return self._model_to_schema(location)

    async def update_location(
        self, location_id: int, location_data: LocationUpdate
    ) -> Optional[LocationResponse]:
        logger.info(f"Updating location with id: {location_id}")
        query = select(Location).where(Location.id == location_id)
        result = await self.session.execute(query)
        location = result.scalar_one_or_none()

        if location is None:
            logger.warning(f"Location with id {location_id} not found for update")
            return None

        update_data = location_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(location, field, value)

        await self.session.commit()
        await self.session.refresh(location)
        logger.info(f"Successfully updated location with id: {location_id}")
        return self._model_to_schema(location)

    async def delete_location(self, location_id: int) -> bool:
        logger.info(f"Deleting location with id: {location_id}")
        query = delete(Location).where(Location.id == location_id)
        result = await self.session.execute(query)
        await self.session.commit()
        success = result.rowcount > 0
        if success:
            logger.info(f"Successfully deleted location with id: {location_id}")
        else:
            logger.warning(f"Location with id {location_id} not found for deletion")
        return success

    async def search_locations(self, search_term: str) -> List[LocationResponse]:
        logger.info(f"Searching locations with term: {search_term}")
        query = select(Location).where(
            or_(
                Location.name.ilike(f"%{search_term}%"),
                Location.address.ilike(f"%{search_term}%")
            )
        )
        result = await self.session.execute(query)
        locations = result.scalars().all()
        return [self._model_to_schema(location) for location in locations]

    async def get_locations_by_capacity(
        self,
        min_capacity: int | None = None,
        max_capacity: int | None = None
    ) -> List[LocationResponse]:
        logger.info(f"Getting locations by capacity range: {min_capacity} - {max_capacity}")
        query = select(Location)
        
        if min_capacity is not None:
            query = query.where(Location.capacity >= min_capacity)
        if max_capacity is not None:
            query = query.where(Location.capacity <= max_capacity)
            
        result = await self.session.execute(query)
        locations = result.scalars().all()
        return [self._model_to_schema(location) for location in locations] 