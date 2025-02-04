from datetime import datetime
from pydantic import Field, EmailStr
from .base import BaseSchema

class UserBase(BaseSchema):
    """Base schema for user data with common attributes"""
    username: str = Field(..., description="User's unique username", min_length=2, example="johndoe")
    email: EmailStr = Field(..., description="User's email address", example="user@example.com")
    role: str = Field(..., description="User's role (student/organizer)", example="student")

class UserCreate(UserBase):
    """Schema for creating a new user"""
    password: str = Field(
        ...,
        description="User's password (will be hashed)",
        min_length=8,
        example="strongpassword123"
    )

class UserUpdate(BaseSchema):
    """Schema for updating an existing user"""
    username: str | None = Field(None, description="New username")
    email: EmailStr | None = Field(None, description="New email address")
    role: str | None = Field(None, description="New role")
    password: str | None = Field(None, description="New password", min_length=8)

class UserResponse(UserBase):
    """Schema for user response with additional system fields"""
    id: int = Field(..., description="Unique user ID")
    created_at: datetime = Field(..., description="When the user was created") 