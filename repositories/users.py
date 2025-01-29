from typing import List, Optional
import logging
from sqlalchemy import select, or_, delete
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext

from core.models.users import User
from core.schemas.users import UserCreate, UserUpdate, UserResponse

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
logger = logging.getLogger(__name__)

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    def _hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def _model_to_schema(self, user: User) -> UserResponse:
        return UserResponse.model_validate(user)

    async def get_user_by_id(self, user_id: int) -> Optional[UserResponse]:
        logger.info(f"Getting user by id: {user_id}")
        query = select(User).where(User.id == user_id)
        result = await self.session.execute(query)
        user = result.scalar_one_or_none()
        if user is None:
            logger.warning(f"User with id {user_id} not found")
        return self._model_to_schema(user) if user else None

    async def get_user_by_username(self, username: str) -> Optional[UserResponse]:
        logger.info(f"Getting user by username: {username}")
        query = select(User).where(User.username == username)
        result = await self.session.execute(query)
        user = result.scalar_one_or_none()
        if user is None:
            logger.warning(f"User with username {username} not found")
        return self._model_to_schema(user) if user else None

    async def get_user_by_email(self, email: str) -> Optional[UserResponse]:
        logger.info(f"Getting user by email: {email}")
        query = select(User).where(User.email == email)
        result = await self.session.execute(query)
        user = result.scalar_one_or_none()
        if user is None:
            logger.warning(f"User with email {email} not found")
        return self._model_to_schema(user) if user else None

    async def get_all_users(self) -> List[UserResponse]:
        logger.info("Getting all users")
        query = select(User)
        result = await self.session.execute(query)
        users = result.scalars().all()
        return [self._model_to_schema(user) for user in users]

    async def create_user(self, user_data: UserCreate) -> UserResponse:
        logger.info(f"Creating new user with username: {user_data.username}")
        user = User(
            username=user_data.username,
            email=user_data.email,
            password_hash=self._hash_password(user_data.password),
            role=user_data.role
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        logger.info(f"Successfully created user with id: {user.id}")
        return self._model_to_schema(user)

    async def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[UserResponse]:
        logger.info(f"Updating user with id: {user_id}")
        query = select(User).where(User.id == user_id)
        result = await self.session.execute(query)
        user = result.scalar_one_or_none()
        
        if user is None:
            logger.warning(f"User with id {user_id} not found for update")
            return None

        update_data = user_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if field == "password" and value is not None:
                setattr(user, "password_hash", self._hash_password(value))
            else:
                setattr(user, field, value)

        await self.session.commit()
        await self.session.refresh(user)
        logger.info(f"Successfully updated user with id: {user_id}")
        return self._model_to_schema(user)

    async def delete_user(self, user_id: int) -> bool:
        logger.info(f"Deleting user with id: {user_id}")
        query = delete(User).where(User.id == user_id)
        result = await self.session.execute(query)
        await self.session.commit()
        success = result.rowcount > 0
        if success:
            logger.info(f"Successfully deleted user with id: {user_id}")
        else:
            logger.warning(f"User with id {user_id} not found for deletion")
        return success

    async def search_users(self, search_term: str) -> List[UserResponse]:
        logger.info(f"Searching users with term: {search_term}")
        query = select(User).where(
            or_(
                User.username.ilike(f"%{search_term}%"),
                User.email.ilike(f"%{search_term}%"),
                User.role.ilike(f"%{search_term}%")
            )
        )
        
        result = await self.session.execute(query)
        users = result.scalars().all()
        return [self._model_to_schema(user) for user in users]
