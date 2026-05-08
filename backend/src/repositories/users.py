from typing import Sequence

from sqlalchemy import or_, select, update
from sqlalchemy.exc import IntegrityError

from src.models.users import User
from src.repositories.base import DeleteOnlyRepository
from src.repositories.exceptions import UserEmailIsUsingError


class UserRepository(DeleteOnlyRepository[User]):
    model = User

    async def handle_error(self, err: IntegrityError):
        await self.session.rollback()
        orig_err: str = str(err.orig)
        if "users_email_key" in orig_err:
            raise UserEmailIsUsingError
        raise err

    def get_search_expressions(self, search: str | None):
        expressions = []
        if search:
            expressions.append(
                or_(
                    self.model.lastname.icontains(search),
                    self.model.firstname.icontains(search),
                    self.model.middlename.icontains(search),
                )
            )
        return expressions

    async def get(self, pk: int) -> User | None:
        return await self.session.get(self.model, pk)

    async def get_all(
        self,
        search: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> Sequence[User]:
        expressions = self.get_search_expressions(search)
        statement = (
            select(self.model)
            .where(*expressions)
            .limit(limit)
            .offset(offset)
            .order_by(self.model.id)
        )
        res = await self.session.execute(statement)
        return res.scalars().all()

    async def count(
        self, filters: dict[str, int] = {}, search: str | None = None
    ) -> int:
        expressions = self.get_search_expressions(search)
        return await self._count(filters, expressions)

    async def create(self, data: dict) -> User:
        instance = self.model(**data)
        self.session.add(instance)
        try:
            await self.session.commit()
        except IntegrityError as ex:
            await self.handle_error(ex)
        else:
            return instance

    async def update(self, id: int, data: dict) -> User | None:
        statement = (
            update(self.model)
            .where(self.model.id == id)
            .values(**data)
            .returning(self.model)
        )
        try:
            res = await self.session.execute(statement)
            await self.session.commit()
        except IntegrityError as ex:
            await self.handle_error(ex)
        else:
            return res.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        statement = select(self.model).filter_by(email=email)
        res = await self.session.execute(statement)
        return res.scalar_one_or_none()

    async def change_password(self, id: int, new_password_hash: str):
        statement = (
            update(self.model)
            .where(self.model.id == id)
            .values(password=new_password_hash)
        )
        await self.session.execute(statement)
        await self.session.commit()
