from contextlib import asynccontextmanager
from fastapi import FastAPI
from db import create_db_and_tables

from middleware import setup_cors
from routers import answers, questions


@asynccontextmanager
async def lifespan(_app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(questions.router, prefix="/question", tags=["questions"])
app.include_router(answers.router, prefix="/answer", tags=["answers"])

setup_cors(app)
