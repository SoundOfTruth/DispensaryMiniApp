from typing import Generic, Sequence, TypeVar

from sqlalchemy import func, select

from src.database.core import AsyncSession, Base

Table = TypeVar("Table", bound=Base)


class BaseRepository(Generic[Table]):
    model: type[Table]

    def __init__(self, session: AsyncSession):
        self.session = session

    async def _count(self, filters: dict[str, int] = {}, expressions: list = []) -> int:
        statement = (
            select(func.count())
            .select_from(self.model)
            .filter_by(**filters)
            .where(*expressions)
        )
        res = await self.session.execute(statement)
        return res.scalar_one()


class DefaultRepository(BaseRepository[Table]):
    async def get(self, pk: int, options: list = list()):
        return await self.session.get(self.model, pk, options=options)

    async def get_all(
        self,
        expression_args: list = list(),
        filter_kwargs: dict = dict(),
        options: list = list(),
    ) -> Sequence[Table]:
        statement = (
            select(self.model)
            .where(*expression_args)
            .filter_by(**filter_kwargs)
            .options(*options)
        )
        res = await self.session.execute(statement)
        return res.scalars().all()
