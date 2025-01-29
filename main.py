import logging
from contextlib import asynccontextmanager
from typing import Annotated

import uvicorn
from sqlalchemy.exc import OperationalError

from core.models import Base, db_helper
from fastapi import FastAPI, Path
from pydantic import BaseModel, EmailStr


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        async with db_helper.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        yield
        await db_helper.engine.dispose()
    except OperationalError as e:
        logging.error(f"Ошибка подключения к базе данных: {e}")
        raise


app = FastAPI(lifespan=lifespan)


class CreateUser(BaseModel):
    email: EmailStr

class CheckUser(BaseModel):
    access: str


@app.get("/")
def hello_sex():
    return {"message": "sex"}


@app.get("/storm/{kda}/")
def get_storm_kda(kda: int):
    return {
        "storm": {
            "kda": kda,
        },
    }


@app.get("/hero/{index}/")
def get_hero_id(index: Annotated[int, Path(ge=1, lt=1_000_000)]):
    return {
        "hero": {
            "id": index,
        },
    }


@app.post("/users/")
def create_user(user: CreateUser):
    return {
        "message": "success",
        "user": user.email,
    }

@app.get("/users/check/")
def check_user(user: CheckUser):
    return {
        "access": True,
    }

@app.get("/users/check/")
def check_user(user: CheckUser):
    return {
        "access": True,
    }


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
