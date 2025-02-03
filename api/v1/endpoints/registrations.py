from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from services.registration_service import RegistrationService
from core.schemas.registrations import RegistrationCreate, RegistrationUpdate, RegistrationResponse
from api.deps import get_registration_service

router = APIRouter(prefix="/registrations", tags=["registrations"])

@router.get("/{registration_id}", response_model=RegistrationResponse)
async def get_registration(
    registration_id: int,
    registration_service: RegistrationService = Depends(get_registration_service)
):
    return await registration_service.get_registration_by_id(registration_id)

@router.get("/", response_model=List[RegistrationResponse])
async def get_registrations(
    registration_service: RegistrationService = Depends(get_registration_service)
):
    return await registration_service.get_all_registrations()

@router.post("/", response_model=RegistrationResponse, status_code=status.HTTP_201_CREATED)
async def create_registration(
    registration_data: RegistrationCreate,
    registration_service: RegistrationService = Depends(get_registration_service)
):
    return await registration_service.create_registration(registration_data)

@router.put("/{registration_id}", response_model=RegistrationResponse)
async def update_registration(
    registration_id: int,
    registration_data: RegistrationUpdate,
    registration_service: RegistrationService = Depends(get_registration_service)
):
    return await registration_service.update_registration(registration_id, registration_data)

@router.delete("/{registration_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_registration(
    registration_id: int,
    registration_service: RegistrationService = Depends(get_registration_service)
):
    await registration_service.delete_registration(registration_id)

@router.get("/user/{user_id}", response_model=List[RegistrationResponse])
async def get_user_registrations(
    user_id: int,
    registration_service: RegistrationService = Depends(get_registration_service)
):
    return await registration_service.get_user_registrations(user_id)

@router.get("/exam/{exam_id}", response_model=List[RegistrationResponse])
async def get_exam_registrations(
    exam_id: int,
    registration_service: RegistrationService = Depends(get_registration_service)
):
    return await registration_service.get_exam_registrations(exam_id)

@router.get("/status/{status}", response_model=List[RegistrationResponse])
async def get_registrations_by_status(
    status: str,
    registration_service: RegistrationService = Depends(get_registration_service)
):
    return await registration_service.get_registrations_by_status(status)

@router.get("/payment-status/{payment_status}", response_model=List[RegistrationResponse])
async def get_registrations_by_payment_status(
    payment_status: str,
    registration_service: RegistrationService = Depends(get_registration_service)
):
    return await registration_service.get_registrations_by_payment_status(payment_status)

@router.get("/check-availability/")
async def check_registration_availability(
    user_id: int,
    exam_id: int,
    registration_service: RegistrationService = Depends(get_registration_service)
):
    return await registration_service.check_registration_availability(user_id, exam_id) 