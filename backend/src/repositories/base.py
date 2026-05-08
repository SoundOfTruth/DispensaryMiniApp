from typing import Any, Sequence, TypeVar

from sqlalchemy import ColumnElement, delete, func, select
from sqlalchemy.exc import IntegrityError

from src.database.core import AsyncSession
from src.database.core import Base as RawBASE
from src.models.mixins import IntPkBase

RawTable = TypeVar("RawTable", bound=RawBASE)
Table = TypeVar("Table", bound=IntPkBase)


class BaseRepository[RawTable]:
    model: type[RawTable]

    def __init__(self, session: AsyncSession):
        self.session = session

    async def _count(
        self, filters: dict[str, Any] = {}, expressions: list[ColumnElement[Any]] = []
    ) -> int:
        statement = (
            select(func.count())
            .select_from(self.model)
            .filter_by(**filters)
            .where(*expressions)
        )
        res = await self.session.execute(statement)
        return res.scalar_one()


class ReadOnlyRepository(BaseRepository[Table]):
    async def get(self, pk: int, options: list = []) -> Table | None:
        return await self.session.get(self.model, pk, options=options)

    async def get_all(
        self,
        expressions: list[ColumnElement[Any]] = [],
        filters: dict[str, Any] = {},
        options: list = [],
    ) -> Sequence[Table]:
        statement = (
            select(self.model)
            .where(*expressions)
            .filter_by(**filters)
            .options(*options)
            .order_by(self.model.id)
        )
        res = await self.session.execute(statement)
        return res.scalars().all()


class DeleteOnlyRepository(BaseRepository[Table]):
    async def handle_error(self, err: IntegrityError):
        await self.session.rollback()
        raise err

    async def delete(self, id: int):
        statement = delete(self.model).where(self.model.id == id)
        try:
            await self.session.execute(statement)
        except IntegrityError as ex:
            await self.handle_error(ex)
        await self.session.commit()

    async def bulk_delete(self, ids: list[int]):
        statement = delete(self.model).where(self.model.id.in_(ids))
        try:
            await self.session.execute(statement)
        except IntegrityError as ex:
            await self.handle_error(ex)
        await self.session.commit()


class DefaultRepository(ReadOnlyRepository[Table], DeleteOnlyRepository[Table]):
    pass
