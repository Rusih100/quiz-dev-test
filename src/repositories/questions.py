from src.models import QuestionModel
from src.repositories.repository import SQLAlchemyRepository


class QuestionRepository(SQLAlchemyRepository):
    model = QuestionModel
