from typing import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_async_session
from repositories.users import UserRepository
from repositories.locations import LocationRepository
from repositories.exams import ExamRepository
from repositories.registrations import RegistrationRepository
from repositories.payments import PaymentRepository
from repositories.results import ResultRepository
from repositories.analytics import AnalyticRepository

from services.user_service import UserService
from services.location_service import LocationService
from services.exam_service import ExamService
from services.registration_service import RegistrationService
from services.payment_service import PaymentService
from services.result_service import ResultService
from services.analytic_service import AnalyticService

# Repositories
async def get_user_repository(db: AsyncSession = Depends(get_async_session)) -> UserRepository:
    return UserRepository(db)

async def get_location_repository(db: AsyncSession = Depends(get_async_session)) -> LocationRepository:
    return LocationRepository(db)

async def get_exam_repository(db: AsyncSession = Depends(get_async_session)) -> ExamRepository:
    return ExamRepository(db)

async def get_registration_repository(db: AsyncSession = Depends(get_async_session)) -> RegistrationRepository:
    return RegistrationRepository(db)

async def get_payment_repository(db: AsyncSession = Depends(get_async_session)) -> PaymentRepository:
    return PaymentRepository(db)

async def get_result_repository(db: AsyncSession = Depends(get_async_session)) -> ResultRepository:
    return ResultRepository(db)

async def get_analytic_repository(db: AsyncSession = Depends(get_async_session)) -> AnalyticRepository:
    return AnalyticRepository(db)

# Services
async def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository)
) -> UserService:
    return UserService(user_repository)

async def get_location_service(
    location_repository: LocationRepository = Depends(get_location_repository)
) -> LocationService:
    return LocationService(location_repository)

async def get_exam_service(
    exam_repository: ExamRepository = Depends(get_exam_repository),
    location_repository: LocationRepository = Depends(get_location_repository)
) -> ExamService:
    return ExamService(exam_repository, location_repository)

async def get_registration_service(
    registration_repository: RegistrationRepository = Depends(get_registration_repository),
    exam_repository: ExamRepository = Depends(get_exam_repository),
    user_repository: UserRepository = Depends(get_user_repository)
) -> RegistrationService:
    return RegistrationService(registration_repository, exam_repository, user_repository)

async def get_payment_service(
    payment_repository: PaymentRepository = Depends(get_payment_repository),
    exam_repository: ExamRepository = Depends(get_exam_repository),
    user_repository: UserRepository = Depends(get_user_repository),
    registration_repository: RegistrationRepository = Depends(get_registration_repository)
) -> PaymentService:
    return PaymentService(
        payment_repository, 
        exam_repository,
        user_repository,
        registration_repository
    )

async def get_result_service(
    result_repository: ResultRepository = Depends(get_result_repository),
    exam_repository: ExamRepository = Depends(get_exam_repository),
    user_repository: UserRepository = Depends(get_user_repository),
    registration_repository: RegistrationRepository = Depends(get_registration_repository)
) -> ResultService:
    return ResultService(
        result_repository,
        exam_repository,
        user_repository,
        registration_repository
    )

async def get_analytic_service(
    analytic_repository: AnalyticRepository = Depends(get_analytic_repository),
    exam_repository: ExamRepository = Depends(get_exam_repository),
    registration_repository: RegistrationRepository = Depends(get_registration_repository),
    result_repository: ResultRepository = Depends(get_result_repository)
) -> AnalyticService:
    return AnalyticService(
        analytic_repository,
        exam_repository,
        registration_repository,
        result_repository
    ) 