from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import SQLModel, Session, create_engine, select
from sqlalchemy import exists

from models import Answer, Question

from middleware import setup_cors


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)
setup_cors(app)


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


@app.post("/question/")
def create_question(question: Question, session: SessionDep) -> Question:
    session.add(question)
    session.commit()
    session.refresh(question)
    return question


@app.get("/question/")
def read_questions(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Question]:
    question = session.exec(select(Question).offset(offset).limit(limit)).all()
    return [*question]


@app.get("/question/{question_id}/")
def read_question(question_id: int, session: SessionDep) -> Question:
    question = session.get(Question, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="question not found")
    return question


@app.post("/answer/")
def create_answer(answer: Answer, session: SessionDep) -> Answer:
    session.add(answer)
    session.commit()
    session.refresh(answer)
    return answer


@app.get("/answer/{answer_id}/")
def read_answer(answer_id: int, session: SessionDep) -> Answer:
    answer = session.get(Answer, answer_id)
    if not answer:
        raise HTTPException(status_code=404, detail="answer not found")
    return answer


@app.get("/question/{question_id}/answers/")
def read_answers_for_question(question_id: int, session: SessionDep) -> list[Answer]:
    question_exists = session.exec(
        select(exists(select(Question).where(Question.id == question_id)))
    ).first()

    if not question_exists:
        raise HTTPException(status_code=404, detail="question not found")

    answer = session.exec(select(Answer).where(Answer.question_id == question_id)).all()
    return [*answer]


@app.get("/question/{question_id}/visit/")
def increment_visits(question_id: int, session: SessionDep) -> int:
    question = session.get(Question, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="question not found")
    question.visits += 1
    session.commit()
    return question.visits
