from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(frozen=True, slots=True)
class Question:
    id: int
    api_id: int
    question: str
    answer: str
    created_at: datetime

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "api_id": self.api_id,
            "question": self.question,
            "answer": self.answer,
            "created_at": self.created_at,
        }
