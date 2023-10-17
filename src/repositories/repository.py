from abc import ABC, abstractmethod
from typing import Any, TypeAlias

from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from src.database.database import async_session_maker
from src.exceptions.repositories import (
    RepositoryError,
    RepositoryIntegrityError,
)

EntityDict: TypeAlias = dict[str, Any]
Entity: TypeAlias = Any


class AbstractRepository(ABC):
    @abstractmethod
    async def get_all(self) -> list[Entity]:
        raise NotImplementedError

    @abstractmethod
    async def get_one(self, **filter_by: Any) -> Entity | None:
        raise NotImplementedError

    @abstractmethod
    async def add_one(self, *, data: EntityDict) -> Entity:
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None
    session_factory = async_session_maker

    async def get_all(self, **filter_by: Any) -> list[Entity]:
        async with self.session_factory() as session:
            query = select(self.model).filter_by(**filter_by)
            try:
                result = await session.execute(query)
            except (SQLAlchemyError, Exception) as exc:
                await session.rollback()
                raise RepositoryError() from exc
            return [item.to_dataclass() for item in result.scalars()]

    async def get_one(self, **filter_by: Any) -> Entity | None:
        async with self.session_factory() as session:
            query = select(self.model).filter_by(**filter_by)
            try:
                result = await session.execute(query)
            except (SQLAlchemyError, Exception) as exc:
                await session.rollback()
                raise RepositoryError() from exc

            if result := result.scalars().first():
                return result.to_dataclass()
            return None

    async def add_one(self, *, data: EntityDict) -> Entity:
        async with self.session_factory() as session:
            query = insert(self.model).values(**data).returning(self.model)
            try:
                result = await session.execute(query)
            except IntegrityError as exc:
                await session.rollback()
                raise RepositoryIntegrityError() from exc
            except (SQLAlchemyError, Exception) as exc:
                await session.rollback()
                raise RepositoryError() from exc

            return result.scalar_one().to_dataclass()
