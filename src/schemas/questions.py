from datetime import datetime

from pydantic import BaseModel, PositiveInt


class QuestionRequestCreateSchema(BaseModel):
    questions_num: PositiveInt


class QuestionReadSchema(BaseModel):
    id: PositiveInt
    api_id: PositiveInt
    question: str
    answer: str
    created_at: datetime


class QuestionListReadSchema(BaseModel):
    count: PositiveInt
    questions: list[QuestionReadSchema]
