import asyncio
import getpass

from pydantic import validate_email

from src.database.core import AsyncSessionLocal
from src.repositories.exceptions import UserEmailIsUsingError
from src.schemas.users import CreateUserSchema, Role
from src.services.users import UserService


def get_password() -> str:
    password = getpass.getpass("Пароль: ")
    password_repeat = getpass.getpass("Пароль (повтор): ")
    if len(password) < 8:
        print("Пароль должен состоять минимум из 8 символов.")
        return get_password()
    if password != password_repeat:
        print("Пароли не совпадают.")
        return get_password()
    return password


async def create_superuser():
    email = input("Почта: ")
    try:
        validate_email(email)
    except Exception:
        print("Введите правельный email.")
        return await create_superuser()
    lastname = input("Фамилия: ")
    firstname = input("Имя: ")
    middlename = input("Отчество: ")
    password = get_password()
    try:
        schema = CreateUserSchema(
            email=email,
            password=password,
            lastname=lastname,
            firstname=firstname,
            middlename=middlename,
            role=Role.SUPERUSER,
        )
    except Exception as ex:
        print(ex)
        return await create_superuser()
    async with AsyncSessionLocal() as session:
        repo = UserService(session)
        try:
            created = await repo.create(schema)
        except UserEmailIsUsingError:
            print("Пользователь с указанным email уже существует.")
        else:
            print("Добавлен superuser, email:", created.email)


def main():
    asyncio.run(create_superuser())
