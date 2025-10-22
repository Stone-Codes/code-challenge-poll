from fastapi import APIRouter
from typing import Annotated
from fastapi import Depends, HTTPException
from sqlmodel import Session

from db import get_session
from models import Answer


router = APIRouter()


SessionDep = Annotated[Session, Depends(get_session)]


@router.post("/")
def create_answer(answer: Answer, session: SessionDep) -> Answer:
    session.add(answer)
    session.commit()
    session.refresh(answer)
    return answer


@router.get("/{answer_id}/")
def read_answer(answer_id: int, session: SessionDep) -> Answer:
    answer = session.get(Answer, answer_id)
    if not answer:
        raise HTTPException(status_code=404, detail="answer not found")
    return answer
