from pydantic import Field
from .base import BaseSchema

class LocationBase(BaseSchema):
    """Base schema for exam location data"""
    name: str = Field(..., description="Name of the location", example="Main Campus Hall A")
    address: str = Field(..., description="Full address of the location", example="123 University Street")
    capacity: int = Field(..., description="Maximum capacity of the location", example=100)

class LocationCreate(LocationBase):
    """Schema for creating a new location"""
    pass

class LocationUpdate(BaseSchema):
    """Schema for updating an existing location"""
    name: str | None = Field(None, description="New location name")
    address: str | None = Field(None, description="New address")
    capacity: int | None = Field(None, description="New maximum capacity")

class LocationResponse(LocationBase):
    """Schema for location response with additional system fields"""
    id: int = Field(..., description="Unique location ID") 