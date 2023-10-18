from abc import ABC, abstractmethod
from typing import Any, TypeAlias

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import SQLAlchemyError

from src.database.database import async_session_maker
from src.exceptions.repositories import RepositoryError

EntityDict: TypeAlias = dict[str, Any]
Entity: TypeAlias = Any


class AbstractRepository(ABC):
    @abstractmethod
    async def get_many_last(self, *, count: int) -> list[Entity]:
        raise NotImplementedError

    @abstractmethod
    async def add_many(self, *, data: list[EntityDict]) -> int:
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None
    session_factory = async_session_maker

    async def get_many_last(self, *, count: int) -> list[Entity]:
        async with self.session_factory() as session:
            query = (
                select(self.model).order_by(self.model.id.desc()).limit(count)
            )
            try:
                result = await session.execute(query)
            except (SQLAlchemyError, Exception) as exc:
                raise RepositoryError() from exc
            items = [item.to_dataclass() for item in result.scalars()]
            if len(items) != count:
                return []
            return items

    async def add_many(self, *, data: list[EntityDict]) -> int:
        async with self.session_factory() as session:
            query = (
                insert(self.model)
                .values(data)
                .on_conflict_do_nothing()
                .returning(self.model.id)
                .execution_options(inline=True, returning=True)
            )
            try:
                result = await session.execute(query)
                await session.commit()
            except (SQLAlchemyError, Exception) as exc:
                await session.rollback()
                raise RepositoryError() from exc
            return len(result.scalars().all())
