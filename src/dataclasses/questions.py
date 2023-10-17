from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class Question:
    id: int
    api_id: int
    question: str
    answer: str
    created_at: datetime
