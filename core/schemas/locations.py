from .base import BaseSchema

class LocationBase(BaseSchema):
    name: str
    address: str
    capacity: int

class LocationCreate(LocationBase):
    pass

class LocationUpdate(BaseSchema):
    name: str | None = None
    address: str | None = None
    capacity: int | None = None

class LocationResponse(LocationBase):
    id: int 