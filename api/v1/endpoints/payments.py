from typing import List, Optional
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, status
from services.payment_service import PaymentService
from core.schemas.payments import PaymentCreate, PaymentUpdate, PaymentResponse
from api.deps import get_payment_service

router = APIRouter(prefix="/payments", tags=["payments"])

@router.get("/{payment_id}", response_model=PaymentResponse)
async def get_payment(
    payment_id: int,
    payment_service: PaymentService = Depends(get_payment_service)
):
    return await payment_service.get_payment_by_id(payment_id)

@router.get("/", response_model=List[PaymentResponse])
async def get_payments(
    payment_service: PaymentService = Depends(get_payment_service)
):
    return await payment_service.get_all_payments()

@router.post("/", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
async def create_payment(
    payment_data: PaymentCreate,
    payment_service: PaymentService = Depends(get_payment_service)
):
    return await payment_service.create_payment(payment_data)

@router.put("/{payment_id}", response_model=PaymentResponse)
async def update_payment(
    payment_id: int,
    payment_data: PaymentUpdate,
    payment_service: PaymentService = Depends(get_payment_service)
):
    return await payment_service.update_payment(payment_id, payment_data)

@router.delete("/{payment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_payment(
    payment_id: int,
    payment_service: PaymentService = Depends(get_payment_service)
):
    await payment_service.delete_payment(payment_id)

@router.get("/user/{user_id}", response_model=List[PaymentResponse])
async def get_user_payments(
    user_id: int,
    payment_service: PaymentService = Depends(get_payment_service)
):
    return await payment_service.get_user_payments(user_id)

@router.get("/exam/{exam_id}", response_model=List[PaymentResponse])
async def get_exam_payments(
    exam_id: int,
    payment_service: PaymentService = Depends(get_payment_service)
):
    return await payment_service.get_exam_payments(exam_id)

@router.get("/status/{status}", response_model=List[PaymentResponse])
async def get_payments_by_status(
    status: str,
    payment_service: PaymentService = Depends(get_payment_service)
):
    return await payment_service.get_payments_by_status(status)

@router.get("/by-amount/", response_model=List[PaymentResponse])
async def get_payments_by_amount_range(
    min_amount: Optional[Decimal] = None,
    max_amount: Optional[Decimal] = None,
    payment_service: PaymentService = Depends(get_payment_service)
):
    return await payment_service.get_payments_by_amount_range(
        min_amount=min_amount,
        max_amount=max_amount
    )

@router.post("/{payment_id}/refund", response_model=PaymentResponse)
async def process_refund(
    payment_id: int,
    payment_service: PaymentService = Depends(get_payment_service)
):
    return await payment_service.process_refund(payment_id) 