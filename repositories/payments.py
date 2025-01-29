from typing import List, Optional
import logging
from decimal import Decimal
from sqlalchemy import select, or_, delete
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.payments import Payment
from core.schemas.payments import PaymentCreate, PaymentUpdate, PaymentResponse

logger = logging.getLogger(__name__)

class PaymentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    def _model_to_schema(self, payment: Payment) -> PaymentResponse:
        return PaymentResponse.model_validate(payment)

    async def get_payment_by_id(self, payment_id: int) -> Optional[PaymentResponse]:
        logger.info(f"Getting payment by id: {payment_id}")
        query = select(Payment).where(Payment.id == payment_id)
        result = await self.session.execute(query)
        payment = result.scalar_one_or_none()
        if payment is None:
            logger.warning(f"Payment with id {payment_id} not found")
        return self._model_to_schema(payment) if payment else None

    async def get_all_payments(self) -> List[PaymentResponse]:
        logger.info("Getting all payments")
        query = select(Payment)
        result = await self.session.execute(query)
        payments = result.scalars().all()
        return [self._model_to_schema(payment) for payment in payments]

    async def create_payment(self, payment_data: PaymentCreate) -> PaymentResponse:
        logger.info(f"Creating new payment for user {payment_data.user_id} and exam {payment_data.exam_id}")
        payment = Payment(**payment_data.model_dump())
        self.session.add(payment)
        await self.session.commit()
        await self.session.refresh(payment)
        logger.info(f"Successfully created payment with id: {payment.id}")
        return self._model_to_schema(payment)

    async def update_payment(
        self, payment_id: int, payment_data: PaymentUpdate
    ) -> Optional[PaymentResponse]:
        logger.info(f"Updating payment with id: {payment_id}")
        query = select(Payment).where(Payment.id == payment_id)
        result = await self.session.execute(query)
        payment = result.scalar_one_or_none()

        if payment is None:
            logger.warning(f"Payment with id {payment_id} not found for update")
            return None

        update_data = payment_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(payment, field, value)

        await self.session.commit()
        await self.session.refresh(payment)
        logger.info(f"Successfully updated payment with id: {payment_id}")
        return self._model_to_schema(payment)

    async def delete_payment(self, payment_id: int) -> bool:
        logger.info(f"Deleting payment with id: {payment_id}")
        query = delete(Payment).where(Payment.id == payment_id)
        result = await self.session.execute(query)
        await self.session.commit()
        success = result.rowcount > 0
        if success:
            logger.info(f"Successfully deleted payment with id: {payment_id}")
        else:
            logger.warning(f"Payment with id {payment_id} not found for deletion")
        return success

    async def get_user_payments(self, user_id: int) -> List[PaymentResponse]:
        logger.info(f"Getting payments for user: {user_id}")
        query = select(Payment).where(Payment.user_id == user_id)
        result = await self.session.execute(query)
        payments = result.scalars().all()
        return [self._model_to_schema(payment) for payment in payments]

    async def get_exam_payments(self, exam_id: int) -> List[PaymentResponse]:
        logger.info(f"Getting payments for exam: {exam_id}")
        query = select(Payment).where(Payment.exam_id == exam_id)
        result = await self.session.execute(query)
        payments = result.scalars().all()
        return [self._model_to_schema(payment) for payment in payments]

    async def get_payments_by_status(self, status: str) -> List[PaymentResponse]:
        logger.info(f"Getting payments by status: {status}")
        query = select(Payment).where(Payment.status == status)
        result = await self.session.execute(query)
        payments = result.scalars().all()
        return [self._model_to_schema(payment) for payment in payments]

    async def get_payments_by_amount_range(
        self,
        min_amount: Decimal | None = None,
        max_amount: Decimal | None = None
    ) -> List[PaymentResponse]:
        logger.info(f"Getting payments by amount range: {min_amount} - {max_amount}")
        query = select(Payment)
        
        if min_amount is not None:
            query = query.where(Payment.amount >= min_amount)
        if max_amount is not None:
            query = query.where(Payment.amount <= max_amount)
            
        result = await self.session.execute(query)
        payments = result.scalars().all()
        return [self._model_to_schema(payment) for payment in payments]

    async def get_user_exam_payment(self, user_id: int, exam_id: int) -> Optional[PaymentResponse]:
        logger.info(f"Getting payment for user {user_id} and exam {exam_id}")
        query = select(Payment).where(
            Payment.user_id == user_id,
            Payment.exam_id == exam_id
        )
        result = await self.session.execute(query)
        payment = result.scalar_one_or_none()
        if payment is None:
            logger.warning(f"Payment not found for user {user_id} and exam {exam_id}")
        return self._model_to_schema(payment) if payment else None 