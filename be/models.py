from sqlmodel import Field, SQLModel


class Question(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    text: str = Field(index=True)
    visits: int = Field(default=0)


class QuestionCreate(SQLModel):
    text: str


class Answer(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    question_id: int = Field(foreign_key="question.id")
    text: str = Field(index=True)


class AnswerCreate(SQLModel):
    question_id: int
    text: str
