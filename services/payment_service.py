from typing import List, Optional
from datetime import datetime
from decimal import Decimal
import logging
from fastapi import HTTPException, status

from repositories.payments import PaymentRepository
from repositories.exams import ExamRepository
from repositories.users import UserRepository
from repositories.registrations import RegistrationRepository
from core.schemas.payments import PaymentCreate, PaymentUpdate, PaymentResponse

logger = logging.getLogger(__name__)

class PaymentService:
    def __init__(
        self,
        payment_repository: PaymentRepository,
        exam_repository: ExamRepository,
        user_repository: UserRepository,
        registration_repository: RegistrationRepository
    ):
        self.payment_repository = payment_repository
        self.exam_repository = exam_repository
        self.user_repository = user_repository
        self.registration_repository = registration_repository

    async def get_payment_by_id(self, payment_id: int) -> PaymentResponse:
        payment = await self.payment_repository.get_payment_by_id(payment_id)
        if not payment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Payment with id {payment_id} not found"
            )
        return payment

    async def get_all_payments(self) -> List[PaymentResponse]:
        return await self.payment_repository.get_all_payments()

    async def create_payment(self, payment_data: PaymentCreate) -> PaymentResponse:
        # Проверка существования пользователя
        user = await self.user_repository.get_user_by_id(payment_data.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {payment_data.user_id} not found"
            )

        # Проверка существования экзамена
        exam = await self.exam_repository.get_exam_by_id(payment_data.exam_id)
        if not exam:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Exam with id {payment_data.exam_id} not found"
            )

        # Проверка регистрации на экзамен
        registration = await self.registration_repository.get_user_exam_registration(
            payment_data.user_id,
            payment_data.exam_id
        )
        if not registration:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is not registered for this exam"
            )

        # Проверка существующего платежа
        existing_payment = await self.payment_repository.get_user_exam_payment(
            payment_data.user_id,
            payment_data.exam_id
        )
        if existing_payment:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Payment already exists for this registration"
            )

        # Проверка суммы платежа
        if payment_data.amount != exam.price:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Payment amount must be equal to exam price: {exam.price}"
            )

        # Проверка статуса платежа
        if payment_data.status not in ["pending", "completed", "failed", "refunded"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid payment status"
            )

        return await self.payment_repository.create_payment(payment_data)

    async def update_payment(
        self, payment_id: int, payment_data: PaymentUpdate
    ) -> PaymentResponse:
        # Проверка существования платежа
        current_payment = await self.get_payment_by_id(payment_id)

        # Проверка статуса платежа
        if payment_data.status and payment_data.status not in ["pending", "completed", "failed", "refunded"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid payment status"
            )

        # Обновление статуса регистрации при успешной оплате
        if payment_data.status == "completed":
            registration = await self.registration_repository.get_user_exam_registration(
                current_payment.user_id,
                current_payment.exam_id
            )
            if registration:
                await self.registration_repository.update_registration(
                    registration.id,
                    {"payment_status": "paid"}
                )

        updated_payment = await self.payment_repository.update_payment(payment_id, payment_data)
        if not updated_payment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Payment with id {payment_id} not found"
            )
        return updated_payment

    async def delete_payment(self, payment_id: int) -> bool:
        # Проверка существования платежа
        payment = await self.get_payment_by_id(payment_id)
        
        # Проверка возможности удаления (например, нельзя удалить завершенный платеж)
        if payment.status == "completed":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete completed payment"
            )

        return await self.payment_repository.delete_payment(payment_id)

    async def get_user_payments(self, user_id: int) -> List[PaymentResponse]:
        # Проверка существования пользователя
        user = await self.user_repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found"
            )
        return await self.payment_repository.get_user_payments(user_id)

    async def get_exam_payments(self, exam_id: int) -> List[PaymentResponse]:
        # Проверка существования экзамена
        exam = await self.exam_repository.get_exam_by_id(exam_id)
        if not exam:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Exam with id {exam_id} not found"
            )
        return await self.payment_repository.get_exam_payments(exam_id)

    async def get_payments_by_status(self, status: str) -> List[PaymentResponse]:
        if status not in ["pending", "completed", "failed", "refunded"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid payment status"
            )
        return await self.payment_repository.get_payments_by_status(status)

    async def get_payments_by_amount_range(
        self,
        min_amount: Decimal | None = None,
        max_amount: Decimal | None = None
    ) -> List[PaymentResponse]:
        # Валидация диапазона сумм
        if min_amount is not None and min_amount < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Minimum amount cannot be negative"
            )
        if max_amount is not None and max_amount < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Maximum amount cannot be negative"
            )
        if min_amount is not None and max_amount is not None and min_amount > max_amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Minimum amount cannot be greater than maximum amount"
            )

        return await self.payment_repository.get_payments_by_amount_range(
            min_amount=min_amount,
            max_amount=max_amount
        )

    async def process_refund(self, payment_id: int) -> PaymentResponse:
        """
        Обработка возврата платежа
        """
        payment = await self.get_payment_by_id(payment_id)
        
        if payment.status != "completed":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only completed payments can be refunded"
            )

        # Обновление статуса платежа и регистрации
        updated_payment = await self.update_payment(
            payment_id,
            PaymentUpdate(status="refunded")
        )

        registration = await self.registration_repository.get_user_exam_registration(
            payment.user_id,
            payment.exam_id
        )
        if registration:
            await self.registration_repository.update_registration(
                registration.id,
                {"payment_status": "refunded"}
            )

        return updated_payment 