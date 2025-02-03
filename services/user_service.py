from typing import List, Optional
import logging
from fastapi import HTTPException, status

from repositories.users import UserRepository
from core.schemas.users import UserCreate, UserUpdate, UserResponse

logger = logging.getLogger(__name__)

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_user_by_id(self, user_id: int) -> UserResponse:
        user = await self.user_repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found"
            )
        return user

    async def get_user_by_username(self, username: str) -> Optional[UserResponse]:
        return await self.user_repository.get_user_by_username(username)

    async def get_user_by_email(self, email: str) -> Optional[UserResponse]:
        return await self.user_repository.get_user_by_email(email)

    async def get_all_users(self) -> List[UserResponse]:
        return await self.user_repository.get_all_users()

    async def create_user(self, user_data: UserCreate) -> UserResponse:
        # Проверка на существующего пользователя
        if await self.get_user_by_username(user_data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        if await self.get_user_by_email(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        return await self.user_repository.create_user(user_data)

    async def update_user(self, user_id: int, user_data: UserUpdate) -> UserResponse:
        # Проверка существования пользователя
        await self.get_user_by_id(user_id)
        
        # Проверка уникальности username и email при обновлении
        if user_data.username:
            existing_user = await self.get_user_by_username(user_data.username)
            if existing_user and existing_user.id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already taken"
                )
        
        if user_data.email:
            existing_user = await self.get_user_by_email(user_data.email)
            if existing_user and existing_user.id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )

        updated_user = await self.user_repository.update_user(user_id, user_data)
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found"
            )
        return updated_user

    async def delete_user(self, user_id: int) -> bool:
        # Проверка существования пользователя
        await self.get_user_by_id(user_id)
        return await self.user_repository.delete_user(user_id)

    async def search_users(self, search_term: str) -> List[UserResponse]:
        return await self.user_repository.search_users(search_term) 