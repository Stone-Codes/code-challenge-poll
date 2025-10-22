from fastapi import APIRouter
from typing import Annotated
from fastapi import Depends, HTTPException, Query
from sqlmodel import Session, select
from sqlalchemy import exists

from db import get_session
from models import Answer, Question, QuestionCreate


router = APIRouter()


SessionDep = Annotated[Session, Depends(get_session)]


@router.post("/")
def create_question(question_data: QuestionCreate, session: SessionDep) -> Question:
    db_question = Question(**question_data.model_dump())
    session.add(db_question)
    session.commit()
    session.refresh(db_question)
    return db_question


@router.get("/")
def read_questions(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Question]:
    question = session.exec(select(Question).offset(offset).limit(limit)).all()
    return [*question]


@router.get("/{question_id}/")
def read_question(question_id: int, session: SessionDep) -> Question:
    question = session.get(Question, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="question not found")
    return question


@router.get("/{question_id}/answers/")
def read_answers_for_question(question_id: int, session: SessionDep) -> list[Answer]:
    question_exists = session.exec(
        select(exists(select(Question).where(Question.id == question_id)))
    ).first()

    if not question_exists:
        raise HTTPException(status_code=404, detail="question not found")

    answer = session.exec(select(Answer).where(Answer.question_id == question_id)).all()
    return [*answer]


@router.get("/{question_id}/visit/")
def increment_visits(question_id: int, session: SessionDep) -> int:
    question = session.get(Question, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="question not found")
    question.visits += 1
    session.commit()
    return question.visits
