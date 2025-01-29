from typing import List, Optional
import logging
from sqlalchemy import select, or_, delete
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.results import Result
from core.schemas.results import ResultCreate, ResultUpdate, ResultResponse

logger = logging.getLogger(__name__)

class ResultRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    def _model_to_schema(self, result: Result) -> ResultResponse:
        return ResultResponse.model_validate(result)

    async def get_result_by_id(self, result_id: int) -> Optional[ResultResponse]:
        logger.info(f"Getting result by id: {result_id}")
        query = select(Result).where(Result.id == result_id)
        result = await self.session.execute(query)
        result_obj = result.scalar_one_or_none()
        if result_obj is None:
            logger.warning(f"Result with id {result_id} not found")
        return self._model_to_schema(result_obj) if result_obj else None

    async def get_all_results(self) -> List[ResultResponse]:
        logger.info("Getting all results")
        query = select(Result)
        result = await self.session.execute(query)
        results = result.scalars().all()
        return [self._model_to_schema(r) for r in results]

    async def create_result(self, result_data: ResultCreate) -> ResultResponse:
        logger.info(f"Creating new result for user {result_data.user_id} and exam {result_data.exam_id}")
        result = Result(**result_data.model_dump())
        self.session.add(result)
        await self.session.commit()
        await self.session.refresh(result)
        logger.info(f"Successfully created result with id: {result.id}")
        return self._model_to_schema(result)

    async def update_result(
        self, result_id: int, result_data: ResultUpdate
    ) -> Optional[ResultResponse]:
        logger.info(f"Updating result with id: {result_id}")
        query = select(Result).where(Result.id == result_id)
        result = await self.session.execute(query)
        result_obj = result.scalar_one_or_none()

        if result_obj is None:
            logger.warning(f"Result with id {result_id} not found for update")
            return None

        update_data = result_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(result_obj, field, value)

        await self.session.commit()
        await self.session.refresh(result_obj)
        logger.info(f"Successfully updated result with id: {result_id}")
        return self._model_to_schema(result_obj)

    async def delete_result(self, result_id: int) -> bool:
        logger.info(f"Deleting result with id: {result_id}")
        query = delete(Result).where(Result.id == result_id)
        result = await self.session.execute(query)
        await self.session.commit()
        success = result.rowcount > 0
        if success:
            logger.info(f"Successfully deleted result with id: {result_id}")
        else:
            logger.warning(f"Result with id {result_id} not found for deletion")
        return success

    async def get_user_results(self, user_id: int) -> List[ResultResponse]:
        logger.info(f"Getting results for user: {user_id}")
        query = select(Result).where(Result.user_id == user_id)
        result = await self.session.execute(query)
        results = result.scalars().all()
        return [self._model_to_schema(r) for r in results]

    async def get_exam_results(self, exam_id: int) -> List[ResultResponse]:
        logger.info(f"Getting results for exam: {exam_id}")
        query = select(Result).where(Result.exam_id == exam_id)
        result = await self.session.execute(query)
        results = result.scalars().all()
        return [self._model_to_schema(r) for r in results]

    async def get_user_exam_result(self, user_id: int, exam_id: int) -> Optional[ResultResponse]:
        logger.info(f"Getting result for user {user_id} and exam {exam_id}")
        query = select(Result).where(
            Result.user_id == user_id,
            Result.exam_id == exam_id
        )
        result = await self.session.execute(query)
        result_obj = result.scalar_one_or_none()
        if result_obj is None:
            logger.warning(f"Result not found for user {user_id} and exam {exam_id}")
        return self._model_to_schema(result_obj) if result_obj else None

    async def get_results_by_grade(self, grade: str) -> List[ResultResponse]:
        logger.info(f"Getting results by grade: {grade}")
        query = select(Result).where(Result.grade == grade)
        result = await self.session.execute(query)
        results = result.scalars().all()
        return [self._model_to_schema(r) for r in results]

    async def get_results_by_score_range(
        self,
        min_score: float | None = None,
        max_score: float | None = None
    ) -> List[ResultResponse]:
        logger.info(f"Getting results by score range: {min_score} - {max_score}")
        query = select(Result)
        
        if min_score is not None:
            query = query.where(Result.score >= min_score)
        if max_score is not None:
            query = query.where(Result.score <= max_score)
            
        result = await self.session.execute(query)
        results = result.scalars().all()
        return [self._model_to_schema(r) for r in results] 