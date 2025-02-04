from typing import List, Optional
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, status, Path, Query
from services.payment_service import PaymentService
from core.schemas.payments import PaymentCreate, PaymentUpdate, PaymentResponse
from api.deps import get_payment_service

router = APIRouter(
    prefix="/payments",
    tags=["payments"],
    responses={404: {"description": "Payment not found"}}
)

@router.get(
    "/{payment_id}",
    response_model=PaymentResponse,
    summary="Get payment by ID",
    description="Retrieve detailed information about a specific payment",
    responses={
        200: {"description": "Successfully retrieved payment details"},
        404: {"description": "Payment not found"}
    }
)
async def get_payment(
    payment_id: int = Path(..., description="The ID of the payment to retrieve", gt=0),
    payment_service: PaymentService = Depends(get_payment_service)
):
    """
    Get detailed information about a specific payment, including:
    - Payment amount and status
    - Associated exam and user
    - Payment method details
    - Transaction timestamps
    """
    return await payment_service.get_payment_by_id(payment_id)

@router.get(
    "/",
    response_model=List[PaymentResponse],
    summary="Get all payments",
    description="Retrieve a list of all payments in the system"
)
async def get_payments(
    payment_service: PaymentService = Depends(get_payment_service)
):
    """
    Get a list of all payments:
    - Sorted by date (newest first)
    - Including payment status
    - With transaction details
    """
    return await payment_service.get_all_payments()

@router.post(
    "/",
    response_model=PaymentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create new payment",
    description="Process a new payment for an exam registration",
    responses={
        201: {"description": "Payment processed successfully"},
        400: {"description": "Invalid payment data"},
        404: {"description": "User or exam not found"}
    }
)
async def create_payment(
    payment_data: PaymentCreate,
    payment_service: PaymentService = Depends(get_payment_service)
):
    """
    Process a new payment with validation:
    - Verify exam registration exists
    - Check payment amount matches exam price
    - Validate payment method
    - Process transaction
    """
    return await payment_service.create_payment(payment_data)

@router.put(
    "/{payment_id}",
    response_model=PaymentResponse,
    summary="Update payment",
    description="Update payment details or status",
    responses={
        200: {"description": "Payment updated successfully"},
        404: {"description": "Payment not found"},
        400: {"description": "Invalid update data"}
    }
)
async def update_payment(
    payment_id: int = Path(..., description="The ID of the payment to update", gt=0),
    payment_data: PaymentUpdate = None,
    payment_service: PaymentService = Depends(get_payment_service)
):
    """
    Update payment information:
    - Can modify payment status
    - Update payment method details
    - Add transaction references
    """
    return await payment_service.update_payment(payment_id, payment_data)

@router.delete(
    "/{payment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete payment",
    description="Delete a payment record",
    responses={
        204: {"description": "Payment successfully deleted"},
        404: {"description": "Payment not found"},
        400: {"description": "Cannot delete processed payment"}
    }
)
async def delete_payment(
    payment_id: int = Path(..., description="The ID of the payment to delete", gt=0),
    payment_service: PaymentService = Depends(get_payment_service)
):
    """
    Delete a payment record if:
    - Payment exists
    - Has not been processed
    - Is in a deletable state
    """
    await payment_service.delete_payment(payment_id)

@router.get(
    "/user/{user_id}",
    response_model=List[PaymentResponse],
    summary="Get user payments",
    description="Retrieve all payments made by a specific user"
)
async def get_user_payments(
    user_id: int = Path(..., description="The ID of the user", gt=0),
    payment_service: PaymentService = Depends(get_payment_service)
):
    """
    Get all payments for a specific user:
    - Includes all payment statuses
    - Sorted by date
    - With exam details
    """
    return await payment_service.get_user_payments(user_id)

@router.get(
    "/exam/{exam_id}",
    response_model=List[PaymentResponse],
    summary="Get exam payments",
    description="Retrieve all payments for a specific exam"
)
async def get_exam_payments(
    exam_id: int = Path(..., description="The ID of the exam", gt=0),
    payment_service: PaymentService = Depends(get_payment_service)
):
    """
    Get all payments for a specific exam:
    - Shows payment distribution
    - Includes all payment statuses
    - With user details
    """
    return await payment_service.get_exam_payments(exam_id)

@router.get(
    "/status/{status}",
    response_model=List[PaymentResponse],
    summary="Get payments by status",
    description="Filter payments by their current status"
)
async def get_payments_by_status(
    status: str = Path(..., description="Payment status (e.g., pending, completed, failed)"),
    payment_service: PaymentService = Depends(get_payment_service)
):
    """
    Get payments filtered by status:
    - Supports multiple status types
    - Sorted by date
    - With full payment details
    """
    return await payment_service.get_payments_by_status(status)

@router.get(
    "/by-amount/",
    response_model=List[PaymentResponse],
    summary="Get payments by amount range",
    description="Filter payments based on their amount"
)
async def get_payments_by_amount_range(
    min_amount: Optional[Decimal] = Query(None, description="Minimum payment amount", ge=0),
    max_amount: Optional[Decimal] = Query(None, description="Maximum payment amount", ge=0),
    payment_service: PaymentService = Depends(get_payment_service)
):
    """
    Find payments within amount range:
    - Optional minimum amount
    - Optional maximum amount
    - Sorted by amount
    - Includes all payment statuses
    """
    return await payment_service.get_payments_by_amount_range(
        min_amount=min_amount,
        max_amount=max_amount
    )

@router.post(
    "/{payment_id}/refund",
    response_model=PaymentResponse,
    summary="Process refund",
    description="Process a refund for a completed payment",
    responses={
        200: {"description": "Refund processed successfully"},
        404: {"description": "Payment not found"},
        400: {"description": "Payment cannot be refunded"}
    }
)
async def process_refund(
    payment_id: int = Path(..., description="The ID of the payment to refund", gt=0),
    payment_service: PaymentService = Depends(get_payment_service)
):
    """
    Process a payment refund:
    - Verifies payment is refundable
    - Checks refund eligibility
    - Processes refund transaction
    - Updates payment status
    """
    return await payment_service.process_refund(payment_id) 