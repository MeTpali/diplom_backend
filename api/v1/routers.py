from fastapi import APIRouter
from api.v1.endpoints import (
    users,
    locations,
    exams,
    registrations,
    payments,
    results,
    analytics
)

api_router = APIRouter()

api_router.include_router(users.router)
api_router.include_router(locations.router)
api_router.include_router(exams.router)
api_router.include_router(registrations.router)
api_router.include_router(payments.router)
api_router.include_router(results.router)
api_router.include_router(analytics.router) 