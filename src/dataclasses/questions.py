from dataclasses import dataclass
from datetime import datetime

from src.schemas.questions import QuestionReadSchema


@dataclass(frozen=True, slots=True)
class Question:
    id: int
    api_id: int
    question: str
    answer: str
    created_at: datetime

    def to_read_schema(self) -> QuestionReadSchema:
        return QuestionReadSchema(
            id=self.id,
            api_id=self.api_id,
            question=self.question,
            answer=self.answer,
            created_at=self.created_at,
        )
