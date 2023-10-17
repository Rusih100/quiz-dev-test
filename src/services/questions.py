from collections.abc import Mapping
from datetime import datetime
from logging import getLogger
from typing import Any

from aiohttp import ClientConnectorError
from aiohttp.client import ClientSession

from src.repositories import AbstractRepository

logger = getLogger("QuestionsService")


class QuestionsService:
    def __init__(self, questions_repository: AbstractRepository) -> None:
        self.repository = questions_repository

    @classmethod
    async def _get_question_from_api(cls) -> dict[str, Any] | None:
        url = r"https://jservice.io/api/random?count=1"
        try:
            async with ClientSession() as session:
                response = await session.get(url=url)
                json_response = await response.json()
                return cls._parse_question(json_response=json_response)

        except (ClientConnectorError, Exception) as exc:
            logger.error(exc)
            return None

    @staticmethod
    def _parse_question(
        *, json_response: Mapping[str | int, Any]
    ) -> dict[str, Any]:
        return {
            "api_id": json_response[0]["id"],
            "question": json_response[0]["question"],
            "answer": json_response[0]["answer"],
            "created_at": datetime.strptime(
                json_response[0]["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ"
            ),
        }
