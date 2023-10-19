from typing import Annotated

from fastapi import Depends

from src.repositories import QuestionRepository
from src.services import QuestionsService


def get_questions_service() -> QuestionsService:
    return QuestionsService(QuestionRepository)


QuestionServiceDepends = Annotated[
    QuestionsService, Depends(get_questions_service)
]
