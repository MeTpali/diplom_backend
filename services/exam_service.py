from typing import List, Optional
from datetime import datetime
import logging
from fastapi import HTTPException, status

from repositories.exams import ExamRepository
from repositories.locations import LocationRepository
from core.schemas.exams import ExamCreate, ExamUpdate, ExamResponse

logger = logging.getLogger(__name__)

class ExamService:
    def __init__(
        self,
        exam_repository: ExamRepository,
        location_repository: LocationRepository
    ):
        self.exam_repository = exam_repository
        self.location_repository = location_repository

    async def get_exam_by_id(self, exam_id: int) -> ExamResponse:
        exam = await self.exam_repository.get_exam_by_id(exam_id)
        if not exam:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Exam with id {exam_id} not found"
            )
        return exam

    async def get_all_exams(self) -> List[ExamResponse]:
        return await self.exam_repository.get_all_exams()

    async def create_exam(self, exam_data: ExamCreate) -> ExamResponse:
        # Проверка даты экзамена (не в прошлом)
        if exam_data.date <= datetime.now():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Exam date must be in the future"
            )

        # Проверка существования и доступности локации
        location = await self.location_repository.get_location_by_id(exam_data.location_id)
        if not location:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Location with id {exam_data.location_id} not found"
            )

        # Проверка вместимости локации
        if exam_data.capacity > location.capacity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Exam capacity ({exam_data.capacity}) exceeds location capacity ({location.capacity})"
            )

        # Проверка стоимости экзамена
        if exam_data.price <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Exam price must be positive"
            )

        return await self.exam_repository.create_exam(exam_data)

    async def update_exam(self, exam_id: int, exam_data: ExamUpdate) -> ExamResponse:
        # Проверка существования экзамена
        current_exam = await self.get_exam_by_id(exam_id)

        if exam_data.date and exam_data.date <= datetime.now():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Exam date must be in the future"
            )

        # Проверка локации при её изменении
        if exam_data.location_id:
            location = await self.location_repository.get_location_by_id(exam_data.location_id)
            if not location:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Location with id {exam_data.location_id} not found"
                )
            
            # Проверка вместимости новой локации
            capacity = exam_data.capacity if exam_data.capacity is not None else current_exam.capacity
            if capacity > location.capacity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Exam capacity ({capacity}) exceeds location capacity ({location.capacity})"
                )

        # Проверка цены при её изменении
        if exam_data.price is not None and exam_data.price <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Exam price must be positive"
            )

        updated_exam = await self.exam_repository.update_exam(exam_id, exam_data)
        if not updated_exam:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Exam with id {exam_id} not found"
            )
        return updated_exam

    async def delete_exam(self, exam_id: int) -> bool:
        # Проверка существования экзамена
        await self.get_exam_by_id(exam_id)
        return await self.exam_repository.delete_exam(exam_id)

    async def get_exams_by_subject(self, subject: str) -> List[ExamResponse]:
        return await self.exam_repository.get_exams_by_subject(subject)

    async def get_exams_by_organizer(self, organizer_id: int) -> List[ExamResponse]:
        return await self.exam_repository.get_exams_by_organizer(organizer_id)

    async def get_exams_by_location(self, location_id: int) -> List[ExamResponse]:
        # Проверка существования локации
        location = await self.location_repository.get_location_by_id(location_id)
        if not location:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Location with id {location_id} not found"
            )
        return await self.exam_repository.get_exams_by_location(location_id)

    async def get_upcoming_exams(self) -> List[ExamResponse]:
        return await self.exam_repository.get_upcoming_exams()

    async def search_exams(self, search_term: str) -> List[ExamResponse]:
        return await self.exam_repository.search_exams(search_term)

    async def check_exam_availability(self, exam_id: int) -> bool:
        """
        Проверяет, доступен ли экзамен для регистрации
        """
        exam = await self.get_exam_by_id(exam_id)
        return (
            exam.date > datetime.now() and
            exam.status == "active" and
            exam.current_registrations < exam.capacity
        ) 