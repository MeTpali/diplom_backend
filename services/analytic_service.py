from typing import List, Optional
from datetime import datetime
import logging
from fastapi import HTTPException, status

from repositories.analytics import AnalyticRepository
from repositories.exams import ExamRepository
from repositories.registrations import RegistrationRepository
from repositories.results import ResultRepository
from core.schemas.analytics import AnalyticCreate, AnalyticUpdate, AnalyticResponse

logger = logging.getLogger(__name__)

class AnalyticService:
    def __init__(
        self,
        analytic_repository: AnalyticRepository,
        exam_repository: ExamRepository,
        registration_repository: RegistrationRepository,
        result_repository: ResultRepository
    ):
        self.analytic_repository = analytic_repository
        self.exam_repository = exam_repository
        self.registration_repository = registration_repository
        self.result_repository = result_repository

    async def get_analytic_by_id(self, analytic_id: int) -> AnalyticResponse:
        analytic = await self.analytic_repository.get_analytic_by_id(analytic_id)
        if not analytic:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Analytic with id {analytic_id} not found"
            )
        return analytic

    async def get_all_analytics(self) -> List[AnalyticResponse]:
        return await self.analytic_repository.get_all_analytics()

    async def create_analytic(self, analytic_data: AnalyticCreate) -> AnalyticResponse:
        # Проверка существования экзамена
        exam = await self.exam_repository.get_exam_by_id(analytic_data.exam_id)
        if not exam:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Exam with id {analytic_data.exam_id} not found"
            )

        # Проверка существующей аналитики
        existing_analytic = await self.analytic_repository.get_exam_analytics(
            analytic_data.exam_id
        )
        if existing_analytic:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Analytics already exists for this exam"
            )

        return await self.analytic_repository.create_analytic(analytic_data)

    async def update_analytic(
        self, analytic_id: int, analytic_data: AnalyticUpdate
    ) -> AnalyticResponse:
        # Проверка существования аналитики
        await self.get_analytic_by_id(analytic_id)

        updated_analytic = await self.analytic_repository.update_analytic(
            analytic_id, analytic_data
        )
        if not updated_analytic:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Analytic with id {analytic_id} not found"
            )
        return updated_analytic

    async def delete_analytic(self, analytic_id: int) -> bool:
        # Проверка существования аналитики
        await self.get_analytic_by_id(analytic_id)
        return await self.analytic_repository.delete_analytic(analytic_id)

    async def generate_exam_analytics(self, exam_id: int) -> AnalyticResponse:
        """
        Генерирует аналитику для конкретного экзамена
        """
        # Проверка существования экзамена
        exam = await self.exam_repository.get_exam_by_id(exam_id)
        if not exam:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Exam with id {exam_id} not found"
            )

        # Получение всех регистраций для экзамена
        registrations = await self.registration_repository.get_exam_registrations(exam_id)
        total_registrations = len(registrations)
        
        # Подсчет оплаченных и неоплаченных регистраций
        total_paid = len([r for r in registrations if r.payment_status == "paid"])
        total_unpaid = total_registrations - total_paid

        # Расчет среднего балла
        results = await self.result_repository.get_exam_results(exam_id)
        average_score = None
        if results:
            scores = [r.score for r in results if r.score is not None]
            if scores:
                average_score = sum(scores) / len(scores)

        # Создание или обновление аналитики
        analytic_data = AnalyticCreate(
            exam_id=exam_id,
            total_registrations=total_registrations,
            total_paid=total_paid,
            total_unpaid=total_unpaid,
            average_score=average_score
        )

        existing_analytic = await self.analytic_repository.get_exam_analytics(exam_id)
        if existing_analytic:
            return await self.update_analytic(
                existing_analytic[0].id,
                AnalyticUpdate(**analytic_data.model_dump())
            )
        else:
            return await self.create_analytic(analytic_data)

    async def get_analytics_by_score_range(
        self,
        min_score: float | None = None,
        max_score: float | None = None
    ) -> List[AnalyticResponse]:
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

        return await self.analytic_repository.get_analytics_by_score_range(
            min_score=min_score,
            max_score=max_score
        )

    async def get_analytics_by_registration_count(
        self,
        min_registrations: int | None = None,
        max_registrations: int | None = None
    ) -> List[AnalyticResponse]:
        # Валидация диапазона регистраций
        if min_registrations is not None and min_registrations < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Minimum registrations cannot be negative"
            )
        if max_registrations is not None and max_registrations < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Maximum registrations cannot be negative"
            )
        if min_registrations is not None and max_registrations is not None and min_registrations > max_registrations:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Minimum registrations cannot be greater than maximum registrations"
            )

        return await self.analytic_repository.get_analytics_by_registration_count(
            min_registrations=min_registrations,
            max_registrations=max_registrations
        )

    async def get_analytics_by_payment_ratio(
        self, min_ratio: float | None = None
    ) -> List[AnalyticResponse]:
        # Валидация коэффициента оплаты
        if min_ratio is not None and (min_ratio < 0 or min_ratio > 1):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Payment ratio must be between 0 and 1"
            )

        return await self.analytic_repository.get_analytics_by_payment_ratio(min_ratio) 