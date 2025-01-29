from typing import List, Optional
import logging
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.analytics import Analytic
from core.schemas.analytics import AnalyticCreate, AnalyticUpdate, AnalyticResponse

logger = logging.getLogger(__name__)

class AnalyticRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    def _model_to_schema(self, analytic: Analytic) -> AnalyticResponse:
        return AnalyticResponse.model_validate(analytic)

    async def get_analytic_by_id(self, analytic_id: int) -> Optional[AnalyticResponse]:
        logger.info(f"Getting analytic by id: {analytic_id}")
        query = select(Analytic).where(Analytic.id == analytic_id)
        result = await self.session.execute(query)
        analytic = result.scalar_one_or_none()
        if analytic is None:
            logger.warning(f"Analytic with id {analytic_id} not found")
        return self._model_to_schema(analytic) if analytic else None

    async def get_all_analytics(self) -> List[AnalyticResponse]:
        logger.info("Getting all analytics")
        query = select(Analytic)
        result = await self.session.execute(query)
        analytics = result.scalars().all()
        return [self._model_to_schema(analytic) for analytic in analytics]

    async def create_analytic(self, analytic_data: AnalyticCreate) -> AnalyticResponse:
        logger.info(f"Creating new analytic for exam {analytic_data.exam_id}")
        analytic = Analytic(**analytic_data.model_dump())
        self.session.add(analytic)
        await self.session.commit()
        await self.session.refresh(analytic)
        logger.info(f"Successfully created analytic with id: {analytic.id}")
        return self._model_to_schema(analytic)

    async def update_analytic(
        self, analytic_id: int, analytic_data: AnalyticUpdate
    ) -> Optional[AnalyticResponse]:
        logger.info(f"Updating analytic with id: {analytic_id}")
        query = select(Analytic).where(Analytic.id == analytic_id)
        result = await self.session.execute(query)
        analytic = result.scalar_one_or_none()

        if analytic is None:
            logger.warning(f"Analytic with id {analytic_id} not found for update")
            return None

        update_data = analytic_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(analytic, field, value)

        await self.session.commit()
        await self.session.refresh(analytic)
        logger.info(f"Successfully updated analytic with id: {analytic_id}")
        return self._model_to_schema(analytic)

    async def delete_analytic(self, analytic_id: int) -> bool:
        logger.info(f"Deleting analytic with id: {analytic_id}")
        query = delete(Analytic).where(Analytic.id == analytic_id)
        result = await self.session.execute(query)
        await self.session.commit()
        success = result.rowcount > 0
        if success:
            logger.info(f"Successfully deleted analytic with id: {analytic_id}")
        else:
            logger.warning(f"Analytic with id {analytic_id} not found for deletion")
        return success

    async def get_exam_analytics(self, exam_id: int) -> Optional[AnalyticResponse]:
        logger.info(f"Getting analytics for exam: {exam_id}")
        query = select(Analytic).where(Analytic.exam_id == exam_id)
        result = await self.session.execute(query)
        analytic = result.scalar_one_or_none()
        if analytic is None:
            logger.warning(f"Analytics not found for exam {exam_id}")
        return self._model_to_schema(analytic) if analytic else None

    async def get_analytics_by_score_range(
        self,
        min_score: float | None = None,
        max_score: float | None = None
    ) -> List[AnalyticResponse]:
        logger.info(f"Getting analytics by average score range: {min_score} - {max_score}")
        query = select(Analytic)
        
        if min_score is not None:
            query = query.where(Analytic.average_score >= min_score)
        if max_score is not None:
            query = query.where(Analytic.average_score <= max_score)
            
        result = await self.session.execute(query)
        analytics = result.scalars().all()
        return [self._model_to_schema(analytic) for analytic in analytics]

    async def get_analytics_by_registration_count(
        self,
        min_registrations: int | None = None,
        max_registrations: int | None = None
    ) -> List[AnalyticResponse]:
        logger.info(f"Getting analytics by registration count range: {min_registrations} - {max_registrations}")
        query = select(Analytic)
        
        if min_registrations is not None:
            query = query.where(Analytic.total_registrations >= min_registrations)
        if max_registrations is not None:
            query = query.where(Analytic.total_registrations <= max_registrations)
            
        result = await self.session.execute(query)
        analytics = result.scalars().all()
        return [self._model_to_schema(analytic) for analytic in analytics]

    async def get_analytics_by_payment_ratio(
        self, min_ratio: float | None = None
    ) -> List[AnalyticResponse]:
        logger.info(f"Getting analytics by payment ratio >= {min_ratio}")
        query = select(Analytic)
        
        if min_ratio is not None:
            # Вычисляем соотношение оплаченных к общему количеству регистраций
            query = query.where(
                (Analytic.total_paid / Analytic.total_registrations) >= min_ratio
            )
            
        result = await self.session.execute(query)
        analytics = result.scalars().all()
        return [self._model_to_schema(analytic) for analytic in analytics] 