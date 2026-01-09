from typing import Generic, Sequence, TypeVar

from sqlalchemy import select

from src.database.core import AsyncSession, Base

Table = TypeVar("Table", bound=Base)


class BaseRepository(Generic[Table]):
    model: type[Table]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session


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
