from fastapi import APIRouter, status
from fastapi.background import BackgroundTasks

from src.api.dependencies import QuestionServiceDepends
from src.schemas.questions import (
    QuestionListReadSchema,
    QuestionRequestCreateSchema,
)

router = APIRouter(prefix="/questions", tags=["Questions"])


@router.post(
    "",
    response_model=QuestionListReadSchema,
    summary="Получение вопросов из публичного API",
    description=(
        "Запрашивает вопросы из публичного API и сохраняет их в базе данных. "
        "Возвращает предыдущие сохраненные вопросы из базы данных.<br><br>"
        "**questions_num** - количество запрашиваемых вопросов."
    ),
    status_code=status.HTTP_202_ACCEPTED,
)
async def create_question(
    question_service: QuestionServiceDepends,
    request_body: QuestionRequestCreateSchema,
    background_tasks: BackgroundTasks,
) -> QuestionListReadSchema:
    return await question_service.create_question(
        request_body=request_body,
        background_tasks=background_tasks,
    )
