from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from services.user_service import UserService
from core.schemas.users import UserCreate, UserUpdate, UserResponse
from api.deps import get_user_service

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service)
):
    return await user_service.get_user_by_id(user_id)

@router.get("/", response_model=List[UserResponse])
async def get_users(
    user_service: UserService = Depends(get_user_service)
):
    return await user_service.get_all_users()

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    user_service: UserService = Depends(get_user_service)
):
    return await user_service.create_user(user_data)

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    user_service: UserService = Depends(get_user_service)
):
    return await user_service.update_user(user_id, user_data)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service)
):
    await user_service.delete_user(user_id)

@router.get("/search/{search_term}", response_model=List[UserResponse])
async def search_users(
    search_term: str,
    user_service: UserService = Depends(get_user_service)
):
    return await user_service.search_users(search_term)