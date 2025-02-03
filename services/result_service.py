from typing import List, Optional
from datetime import datetime
import logging
from fastapi import HTTPException, status

from repositories.results import ResultRepository
from repositories.exams import ExamRepository
from repositories.users import UserRepository
from repositories.registrations import RegistrationRepository
from core.schemas.results import ResultCreate, ResultUpdate, ResultResponse

logger = logging.getLogger(__name__)

class ResultService:
    def __init__(
        self,
        result_repository: ResultRepository,
        exam_repository: ExamRepository,
        user_repository: UserRepository,
        registration_repository: RegistrationRepository
    ):
        self.result_repository = result_repository
        self.exam_repository = exam_repository
        self.user_repository = user_repository
        self.registration_repository = registration_repository

    async def get_result_by_id(self, result_id: int) -> ResultResponse:
        result = await self.result_repository.get_result_by_id(result_id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Result with id {result_id} not found"
            )
        return result

    async def get_all_results(self) -> List[ResultResponse]:
        return await self.result_repository.get_all_results()

    async def create_result(self, result_data: ResultCreate) -> ResultResponse:
        # Проверка существования пользователя
        user = await self.user_repository.get_user_by_id(result_data.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {result_data.user_id} not found"
            )

        # Проверка существования экзамена
        exam = await self.exam_repository.get_exam_by_id(result_data.exam_id)
        if not exam:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Exam with id {result_data.exam_id} not found"
            )

        # Проверка регистрации на экзамен
        registration = await self.registration_repository.get_user_exam_registration(
            result_data.user_id,
            result_data.exam_id
        )
        if not registration:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is not registered for this exam"
            )

        # Проверка статуса регистрации
        if registration.status != "confirmed":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Registration is not confirmed"
            )

        # Проверка существующего результата
        existing_result = await self.result_repository.get_user_exam_result(
            result_data.user_id,
            result_data.exam_id
        )
        if existing_result:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Result already exists for this user and exam"
            )

        # Валидация оценки
        if result_data.score is not None and (result_data.score < 0 or result_data.score > 100):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Score must be between 0 and 100"
            )

        return await self.result_repository.create_result(result_data)

    async def update_result(
        self, result_id: int, result_data: ResultUpdate
    ) -> ResultResponse:
        # Проверка существования результата
        current_result = await self.get_result_by_id(result_id)

        # Валидация оценки при обновлении
        if result_data.score is not None and (result_data.score < 0 or result_data.score > 100):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Score must be between 0 and 100"
            )

        # Проверка корректности оценки
        if result_data.grade is not None and result_data.grade not in ["A", "B", "C", "D", "F"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid grade value"
            )

        updated_result = await self.result_repository.update_result(result_id, result_data)
        if not updated_result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Result with id {result_id} not found"
            )
        return updated_result

    async def delete_result(self, result_id: int) -> bool:
        # Проверка существования результата
        await self.get_result_by_id(result_id)
        return await self.result_repository.delete_result(result_id)

    async def get_user_results(self, user_id: int) -> List[ResultResponse]:
        # Проверка существования пользователя
        user = await self.user_repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found"
            )
        return await self.result_repository.get_user_results(user_id)

    async def get_exam_results(self, exam_id: int) -> List[ResultResponse]:
        # Проверка существования экзамена
        exam = await self.exam_repository.get_exam_by_id(exam_id)
        if not exam:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Exam with id {exam_id} not found"
            )
        return await self.result_repository.get_exam_results(exam_id)

    async def get_results_by_grade(self, grade: str) -> List[ResultResponse]:
        if grade not in ["A", "B", "C", "D", "F"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid grade value"
            )
        return await self.result_repository.get_results_by_grade(grade)

    async def get_results_by_score_range(
        self,
        min_score: float | None = None,
        max_score: float | None = None
    ) -> List[ResultResponse]:
        # Валидация диапазона оценок
        if min_score is not None and (min_score < 0 or min_score > 100):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Minimum score must be between 0 and 100"
            )
        if max_score is not None and (max_score < 0 or max_score > 100):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Maximum score must be between 0 and 100"
            )
        if min_score is not None and max_score is not None and min_score > max_score:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Minimum score cannot be greater than maximum score"
            )

        return await self.result_repository.get_results_by_score_range(
            min_score=min_score,
            max_score=max_score
        )

    async def calculate_grade(self, score: float) -> str:
        """
        Вычисляет оценку на основе числового результата
        """
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "F" 