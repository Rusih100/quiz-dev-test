from datetime import datetime
from logging import getLogger
from typing import Any

from aiohttp import ClientConnectorError
from aiohttp.client import ClientSession
from fastapi.background import BackgroundTasks

from src.exceptions.repositories import RepositoryError
from src.repositories import AbstractRepository
from src.schemas.questions import (
    QuestionListReadSchema,
    QuestionRequestCreateSchema,
)

logger = getLogger("QuestionsService")


class QuestionsService:
    def __init__(self, questions_repository: type[AbstractRepository]) -> None:
        self.repository = questions_repository()

    async def create_question(
        self,
        *,
        request_body: QuestionRequestCreateSchema,
        background_tasks: BackgroundTasks,
    ) -> QuestionListReadSchema:
        count = request_body.questions_num
        questions = await self.repository.get_many_last(count=count)
        background_tasks.add_task(self._create_questions_background, count)
        return QuestionListReadSchema(
            count=len(questions),
            questions=[question.to_read_schema() for question in questions],
        )

    async def _create_questions_background(self, count: int) -> None:
        total_added_count = 0
        while total_added_count < count:
            questions = await self._get_questions_from_api(
                count=count - total_added_count
            )
            try:
                added_count = await self.repository.add_many(data=questions)
            except RepositoryError as exc:
                logger.exception(exc)
                break
            print("Добвлено:", added_count)
            total_added_count += added_count

    @classmethod
    async def _get_questions_from_api(
        cls, *, count: int
    ) -> list[dict[str, Any]]:
        url = f"https://jservice.io/api/random?count={count}"
        try:
            async with ClientSession() as session:
                response = await session.get(url=url)
                json_response = await response.json()
                return cls._parse_question(json_response=json_response)
        except (ClientConnectorError, Exception) as exc:
            logger.exception(exc)
            return []

    @staticmethod
    def _parse_question(*, json_response: Any) -> list[dict[str, Any]]:
        questions_list = []
        for question in json_response:
            questions_list.append(
                {
                    "api_id": question["id"],
                    "question": question["question"],
                    "answer": question["answer"],
                    "created_at": datetime.strptime(
                        question["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ"
                    ),
                }
            )
        return questions_list
