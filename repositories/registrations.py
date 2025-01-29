from typing import List, Optional
import logging
from sqlalchemy import select, or_, delete
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.registrations import Registration
from core.schemas.registrations import RegistrationCreate, RegistrationUpdate, RegistrationResponse

logger = logging.getLogger(__name__)

class RegistrationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    def _model_to_schema(self, registration: Registration) -> RegistrationResponse:
        return RegistrationResponse.model_validate(registration)

    async def get_registration_by_id(self, registration_id: int) -> Optional[RegistrationResponse]:
        logger.info(f"Getting registration by id: {registration_id}")
        query = select(Registration).where(Registration.id == registration_id)
        result = await self.session.execute(query)
        registration = result.scalar_one_or_none()
        if registration is None:
            logger.warning(f"Registration with id {registration_id} not found")
        return self._model_to_schema(registration) if registration else None

    async def get_all_registrations(self) -> List[RegistrationResponse]:
        logger.info("Getting all registrations")
        query = select(Registration)
        result = await self.session.execute(query)
        registrations = result.scalars().all()
        return [self._model_to_schema(registration) for registration in registrations]

    async def create_registration(self, registration_data: RegistrationCreate) -> RegistrationResponse:
        logger.info(f"Creating new registration for user {registration_data.user_id} and exam {registration_data.exam_id}")
        registration = Registration(**registration_data.model_dump())
        self.session.add(registration)
        await self.session.commit()
        await self.session.refresh(registration)
        logger.info(f"Successfully created registration with id: {registration.id}")
        return self._model_to_schema(registration)

    async def update_registration(
        self, registration_id: int, registration_data: RegistrationUpdate
    ) -> Optional[RegistrationResponse]:
        logger.info(f"Updating registration with id: {registration_id}")
        query = select(Registration).where(Registration.id == registration_id)
        result = await self.session.execute(query)
        registration = result.scalar_one_or_none()

        if registration is None:
            logger.warning(f"Registration with id {registration_id} not found for update")
            return None

        update_data = registration_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(registration, field, value)

        await self.session.commit()
        await self.session.refresh(registration)
        logger.info(f"Successfully updated registration with id: {registration_id}")
        return self._model_to_schema(registration)

    async def delete_registration(self, registration_id: int) -> bool:
        logger.info(f"Deleting registration with id: {registration_id}")
        query = delete(Registration).where(Registration.id == registration_id)
        result = await self.session.execute(query)
        await self.session.commit()
        success = result.rowcount > 0
        if success:
            logger.info(f"Successfully deleted registration with id: {registration_id}")
        else:
            logger.warning(f"Registration with id {registration_id} not found for deletion")
        return success

    async def get_user_registrations(self, user_id: int) -> List[RegistrationResponse]:
        logger.info(f"Getting registrations for user: {user_id}")
        query = select(Registration).where(Registration.user_id == user_id)
        result = await self.session.execute(query)
        registrations = result.scalars().all()
        return [self._model_to_schema(registration) for registration in registrations]

    async def get_exam_registrations(self, exam_id: int) -> List[RegistrationResponse]:
        logger.info(f"Getting registrations for exam: {exam_id}")
        query = select(Registration).where(Registration.exam_id == exam_id)
        result = await self.session.execute(query)
        registrations = result.scalars().all()
        return [self._model_to_schema(registration) for registration in registrations]

    async def get_registrations_by_status(self, status: str) -> List[RegistrationResponse]:
        logger.info(f"Getting registrations by status: {status}")
        query = select(Registration).where(Registration.status == status)
        result = await self.session.execute(query)
        registrations = result.scalars().all()
        return [self._model_to_schema(registration) for registration in registrations]

    async def get_registrations_by_payment_status(self, payment_status: str) -> List[RegistrationResponse]:
        logger.info(f"Getting registrations by payment status: {payment_status}")
        query = select(Registration).where(Registration.payment_status == payment_status)
        result = await self.session.execute(query)
        registrations = result.scalars().all()
        return [self._model_to_schema(registration) for registration in registrations]

    async def get_user_exam_registration(self, user_id: int, exam_id: int) -> Optional[RegistrationResponse]:
        logger.info(f"Getting registration for user {user_id} and exam {exam_id}")
        query = select(Registration).where(
            Registration.user_id == user_id,
            Registration.exam_id == exam_id
        )
        result = await self.session.execute(query)
        registration = result.scalar_one_or_none()
        if registration is None:
            logger.warning(f"Registration not found for user {user_id} and exam {exam_id}")
        return self._model_to_schema(registration) if registration else None 