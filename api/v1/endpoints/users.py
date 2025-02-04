from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Path, Query
from services.user_service import UserService
from core.schemas.users import UserCreate, UserUpdate, UserResponse
from api.deps import get_user_service

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "User not found"}}
)

@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get user by ID",
    description="Retrieve detailed information about a specific user",
    responses={
        200: {"description": "Successfully retrieved user details"},
        404: {"description": "User not found"}
    }
)
async def get_user(
    user_id: int = Path(..., description="The ID of the user to retrieve", gt=0),
    user_service: UserService = Depends(get_user_service)
):
    """
    Get detailed information about a specific user, including:
    - Personal information
    - Contact details
    - Registration history
    - Exam results summary
    """
    return await user_service.get_user_by_id(user_id)

@router.get(
    "/",
    response_model=List[UserResponse],
    summary="Get all users",
    description="Retrieve a list of all registered users"
)
async def get_users(
    user_service: UserService = Depends(get_user_service)
):
    """
    Get a list of all users:
    - Sorted alphabetically
    - Including basic information
    - With registration counts
    """
    return await user_service.get_all_users()

@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create new user",
    description="Register a new user in the system",
    responses={
        201: {"description": "User created successfully"},
        400: {"description": "Invalid user data"}
    }
)
async def create_user(
    user_data: UserCreate,
    user_service: UserService = Depends(get_user_service)
):
    """
    Create a new user with validation:
    - Verify unique email
    - Validate contact information
    - Initialize user profile
    - Set up default preferences
    """
    return await user_service.create_user(user_data)

@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Update user",
    description="Update an existing user's information",
    responses={
        200: {"description": "User updated successfully"},
        404: {"description": "User not found"},
        400: {"description": "Invalid update data"}
    }
)
async def update_user(
    user_id: int = Path(..., description="The ID of the user to update", gt=0),
    user_data: UserUpdate = None,
    user_service: UserService = Depends(get_user_service)
):
    """
    Update user information:
    - Modify personal details
    - Update contact information
    - Change preferences
    - Maintain history of changes
    """
    return await user_service.update_user(user_id, user_data)

@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete user",
    description="Remove a user from the system",
    responses={
        204: {"description": "User successfully deleted"},
        404: {"description": "User not found"},
        400: {"description": "Cannot delete user with active registrations"}
    }
)
async def delete_user(
    user_id: int = Path(..., description="The ID of the user to delete", gt=0),
    user_service: UserService = Depends(get_user_service)
):
    """
    Delete a user if:
    - User exists
    - No active registrations
    - No pending payments
    """
    await user_service.delete_user(user_id)

@router.get(
    "/search/{search_term}",
    response_model=List[UserResponse],
    summary="Search users",
    description="Search users by name, email, or phone number",
    responses={
        200: {"description": "Search completed successfully"}
    }
)
async def search_users(
    search_term: str = Path(
        ...,
        description="The search term to look for",
        min_length=2
    ),
    user_service: UserService = Depends(get_user_service)
):
    """
    Search users by keyword:
    - Searches in name, email, and phone
    - Case-insensitive
    - Partial matches supported
    - Returns sorted by relevance
    """
    return await user_service.search_users(search_term)