from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from services.exam_service import ExamService
from core.schemas.exams import ExamCreate, ExamUpdate, ExamResponse
from api.deps import get_exam_service

router = APIRouter(prefix="/exams", tags=["exams"])

@router.get("/{exam_id}", response_model=ExamResponse)
async def get_exam(
    exam_id: int,
    exam_service: ExamService = Depends(get_exam_service)
):
    return await exam_service.get_exam_by_id(exam_id)

@router.get("/", response_model=List[ExamResponse])
async def get_exams(
    exam_service: ExamService = Depends(get_exam_service)
):
    return await exam_service.get_all_exams()

@router.post("/", response_model=ExamResponse, status_code=status.HTTP_201_CREATED)
async def create_exam(
    exam_data: ExamCreate,
    exam_service: ExamService = Depends(get_exam_service)
):
    return await exam_service.create_exam(exam_data)

@router.put("/{exam_id}", response_model=ExamResponse)
async def update_exam(
    exam_id: int,
    exam_data: ExamUpdate,
    exam_service: ExamService = Depends(get_exam_service)
):
    return await exam_service.update_exam(exam_id, exam_data)

@router.delete("/{exam_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_exam(
    exam_id: int,
    exam_service: ExamService = Depends(get_exam_service)
):
    await exam_service.delete_exam(exam_id)

@router.get("/subject/{subject}", response_model=List[ExamResponse])
async def get_exams_by_subject(
    subject: str,
    exam_service: ExamService = Depends(get_exam_service)
):
    return await exam_service.get_exams_by_subject(subject)

@router.get("/organizer/{organizer_id}", response_model=List[ExamResponse])
async def get_exams_by_organizer(
    organizer_id: int,
    exam_service: ExamService = Depends(get_exam_service)
):
    return await exam_service.get_exams_by_organizer(organizer_id)

@router.get("/location/{location_id}", response_model=List[ExamResponse])
async def get_exams_by_location(
    location_id: int,
    exam_service: ExamService = Depends(get_exam_service)
):
    return await exam_service.get_exams_by_location(location_id)

@router.get("/upcoming/", response_model=List[ExamResponse])
async def get_upcoming_exams(
    exam_service: ExamService = Depends(get_exam_service)
):
    return await exam_service.get_upcoming_exams()

@router.get("/search/{search_term}", response_model=List[ExamResponse])
async def search_exams(
    search_term: str,
    exam_service: ExamService = Depends(get_exam_service)
):
    return await exam_service.search_exams(search_term)

@router.get("/{exam_id}/availability")
async def check_exam_availability(
    exam_id: int,
    exam_service: ExamService = Depends(get_exam_service)
):
    return await exam_service.check_exam_availability(exam_id) 