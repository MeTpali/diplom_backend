from typing import List, Optional
from datetime import datetime
import logging
from fastapi import HTTPException, status

from repositories.registrations import RegistrationRepository
from repositories.exams import ExamRepository
from repositories.users import UserRepository
from core.schemas.registrations import RegistrationCreate, RegistrationUpdate, RegistrationResponse

logger = logging.getLogger(__name__)

class RegistrationService:
    def __init__(
        self,
        registration_repository: RegistrationRepository,
        exam_repository: ExamRepository,
        user_repository: UserRepository
    ):
        self.registration_repository = registration_repository
        self.exam_repository = exam_repository
        self.user_repository = user_repository

    async def get_registration_by_id(self, registration_id: int) -> RegistrationResponse:
        registration = await self.registration_repository.get_registration_by_id(registration_id)
        if not registration:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Registration with id {registration_id} not found"
            )
        return registration

    async def get_all_registrations(self) -> List[RegistrationResponse]:
        return await self.registration_repository.get_all_registrations()

    async def create_registration(self, registration_data: RegistrationCreate) -> RegistrationResponse:
        # Проверка существования пользователя
        user = await self.user_repository.get_user_by_id(registration_data.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {registration_data.user_id} not found"
            )

        # Проверка существования экзамена
        exam = await self.exam_repository.get_exam_by_id(registration_data.exam_id)
        if not exam:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Exam with id {registration_data.exam_id} not found"
            )

        # Проверка даты экзамена
        if exam.date <= datetime.now():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot register for past exam"
            )

        # Проверка статуса экзамена
        if exam.status != "active":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot register for inactive exam"
            )

        # Проверка наличия свободных мест
        if exam.current_registrations >= exam.capacity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Exam is fully booked"
            )

        # Проверка существующей регистрации
        existing_registration = await self.registration_repository.get_user_exam_registration(
            registration_data.user_id,
            registration_data.exam_id
        )
        if existing_registration:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is already registered for this exam"
            )

        return await self.registration_repository.create_registration(registration_data)

    async def update_registration(
        self, registration_id: int, registration_data: RegistrationUpdate
    ) -> RegistrationResponse:
        # Проверка существования регистрации
        current_registration = await self.get_registration_by_id(registration_id)

        # Проверка статуса экзамена при обновлении статуса регистрации
        if registration_data.status:
            exam = await self.exam_repository.get_exam_by_id(current_registration.exam_id)
            if exam.date <= datetime.now():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Cannot update registration for past exam"
                )

        updated_registration = await self.registration_repository.update_registration(
            registration_id, registration_data
        )
        if not updated_registration:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Registration with id {registration_id} not found"
            )
        return updated_registration

    async def delete_registration(self, registration_id: int) -> bool:
        # Проверка существования регистрации
        registration = await self.get_registration_by_id(registration_id)
        
        # Проверка возможности удаления (например, нельзя удалить после начала экзамена)
        exam = await self.exam_repository.get_exam_by_id(registration.exam_id)
        if exam.date <= datetime.now():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete registration for past exam"
            )

        return await self.registration_repository.delete_registration(registration_id)

    async def get_user_registrations(self, user_id: int) -> List[RegistrationResponse]:
        # Проверка существования пользователя
        user = await self.user_repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found"
            )
        return await self.registration_repository.get_user_registrations(user_id)

    async def get_exam_registrations(self, exam_id: int) -> List[RegistrationResponse]:
        # Проверка существования экзамена
        exam = await self.exam_repository.get_exam_by_id(exam_id)
        if not exam:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Exam with id {exam_id} not found"
            )
        return await self.registration_repository.get_exam_registrations(exam_id)

    async def get_registrations_by_status(self, status: str) -> List[RegistrationResponse]:
        return await self.registration_repository.get_registrations_by_status(status)

    async def get_registrations_by_payment_status(
        self, payment_status: str
    ) -> List[RegistrationResponse]:
        return await self.registration_repository.get_registrations_by_payment_status(payment_status)

    async def check_registration_availability(
        self, user_id: int, exam_id: int
    ) -> dict[str, bool | str]:
        """
        Проверяет возможность регистрации пользователя на экзамен
        """
        exam = await self.exam_repository.get_exam_by_id(exam_id)
        existing_registration = await self.registration_repository.get_user_exam_registration(
            user_id, exam_id
        )

        if existing_registration:
            return {
                "available": False,
                "reason": "Already registered"
            }
        if exam.date <= datetime.now():
            return {
                "available": False,
                "reason": "Exam date has passed"
            }
        if exam.status != "active":
            return {
                "available": False,
                "reason": "Exam is not active"
            }
        if exam.current_registrations >= exam.capacity:
            return {
                "available": False,
                "reason": "Exam is fully booked"
            }
        
        return {
            "available": True,
            "reason": "Registration available"
        } 