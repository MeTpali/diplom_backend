from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1.routers import api_router
from core.config import settings

description = """
Exam Registration System API helps you manage exams, registrations, and results.

## Features

* **Exams** - Create and manage exams
* **Users** - User management
* **Locations** - Manage exam locations
* **Registrations** - Handle exam registrations
* **Payments** - Process and track payments
* **Results** - Record and retrieve exam results
* **Analytics** - Get insights about exams and performance

## Authentication

All endpoints require authentication using JWT tokens.
"""

app = FastAPI(
    title="Exam System API",
    description="API ответственное за диплом студента Денисова Дениса Эдуардовича",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    contact={
        "name": "Your Name",
        "email": "your.email@example.com",
    },
    license_info={
        "name": "MIT",
    },
    openapi_tags=[
        {
            "name": "users",
            "description": "Operations with users, including creation, updates, and search functionality"
        },
        {
            "name": "exams",
            "description": "Operations with exams, including creation, updates, and various search methods"
        },
        {
            "name": "registrations",
            "description": "Operations with exam registrations, including creation, updates, and status management"
        },
        {
            "name": "results",
            "description": "Operations with exam results, including grades, scores, and statistics"
        },
        {
            "name": "payments",
            "description": "Operations with exam payments, including processing, refunds, and payment history"
        },
        {
            "name": "locations",
            "description": "Operations with exam locations, including creation, updates, and capacity management"
        },
        {
            "name": "analytics",
            "description": "Operations with exam analytics and statistics"
        }
    ]
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры API v1
app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
