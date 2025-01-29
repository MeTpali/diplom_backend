from typing import List, Optional
import logging
from sqlalchemy import select, or_, delete
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from core.models.exams import Exam
from core.schemas.exams import ExamCreate, ExamUpdate, ExamResponse

logger = logging.getLogger(__name__)

class ExamRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    def _model_to_schema(self, exam: Exam) -> ExamResponse:
        return ExamResponse.model_validate(exam)

    async def get_exam_by_id(self, exam_id: int) -> Optional[ExamResponse]:
        logger.info(f"Getting exam by id: {exam_id}")
        query = select(Exam).where(Exam.id == exam_id)
        result = await self.session.execute(query)
        exam = result.scalar_one_or_none()
        if exam is None:
            logger.warning(f"Exam with id {exam_id} not found")
        return self._model_to_schema(exam) if exam else None

    async def get_all_exams(self) -> List[ExamResponse]:
        logger.info("Getting all exams")
        query = select(Exam)
        result = await self.session.execute(query)
        exams = result.scalars().all()
        return [self._model_to_schema(exam) for exam in exams]

    async def create_exam(self, exam_data: ExamCreate) -> ExamResponse:
        logger.info(f"Creating new exam for subject: {exam_data.subject}")
        exam = Exam(**exam_data.model_dump())
        self.session.add(exam)
        await self.session.commit()
        await self.session.refresh(exam)
        logger.info(f"Successfully created exam with id: {exam.id}")
        return self._model_to_schema(exam)

    async def update_exam(
        self, exam_id: int, exam_data: ExamUpdate
    ) -> Optional[ExamResponse]:
        logger.info(f"Updating exam with id: {exam_id}")
        query = select(Exam).where(Exam.id == exam_id)
        result = await self.session.execute(query)
        exam = result.scalar_one_or_none()

        if exam is None:
            logger.warning(f"Exam with id {exam_id} not found for update")
            return None

        update_data = exam_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(exam, field, value)

        await self.session.commit()
        await self.session.refresh(exam)
        logger.info(f"Successfully updated exam with id: {exam_id}")
        return self._model_to_schema(exam)

    async def delete_exam(self, exam_id: int) -> bool:
        logger.info(f"Deleting exam with id: {exam_id}")
        query = delete(Exam).where(Exam.id == exam_id)
        result = await self.session.execute(query)
        await self.session.commit()
        success = result.rowcount > 0
        if success:
            logger.info(f"Successfully deleted exam with id: {exam_id}")
        else:
            logger.warning(f"Exam with id {exam_id} not found for deletion")
        return success

    async def get_exams_by_subject(self, subject: str) -> List[ExamResponse]:
        logger.info(f"Getting exams by subject: {subject}")
        query = select(Exam).where(Exam.subject.ilike(f"%{subject}%"))
        result = await self.session.execute(query)
        exams = result.scalars().all()
        return [self._model_to_schema(exam) for exam in exams]

    async def get_exams_by_organizer(self, organizer_id: int) -> List[ExamResponse]:
        logger.info(f"Getting exams by organizer id: {organizer_id}")
        query = select(Exam).where(Exam.organizer_id == organizer_id)
        result = await self.session.execute(query)
        exams = result.scalars().all()
        return [self._model_to_schema(exam) for exam in exams]

    async def get_exams_by_location(self, location_id: int) -> List[ExamResponse]:
        logger.info(f"Getting exams by location id: {location_id}")
        query = select(Exam).where(Exam.location_id == location_id)
        result = await self.session.execute(query)
        exams = result.scalars().all()
        return [self._model_to_schema(exam) for exam in exams]

    async def get_upcoming_exams(self) -> List[ExamResponse]:
        logger.info("Getting upcoming exams")
        query = select(Exam).where(Exam.date >= datetime.now()).order_by(Exam.date)
        result = await self.session.execute(query)
        exams = result.scalars().all()
        return [self._model_to_schema(exam) for exam in exams]

    async def search_exams(self, search_term: str) -> List[ExamResponse]:
        logger.info(f"Searching exams with term: {search_term}")
        query = select(Exam).where(
            or_(
                Exam.subject.ilike(f"%{search_term}%")
            )
        )
        result = await self.session.execute(query)
        exams = result.scalars().all()
        return [self._model_to_schema(exam) for exam in exams] 