from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from src.dataclasses import Question
from src.models.base import DeclarativeBase


class QuestionModel(DeclarativeBase):
    __tablename__ = "question"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    api_id: Mapped[int] = mapped_column(nullable=False, unique=True)
    question: Mapped[str] = mapped_column(nullable=False)
    answer: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False)

    def __repr__(self) -> str:
        return f"QuestionModel(id={self.id!r}, api_id={self.api_id!r}, created_at={self.created_at!r})"

    def to_dataclass(self) -> Question:
        return Question(
            id=self.id,
            api_id=self.api_id,
            question=self.question,
            answer=self.answer,
            created_at=self.created_at,
        )
