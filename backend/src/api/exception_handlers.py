from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from src.api.exceptions import (
    IssuedExcessUserPermissionsError,
    PermissionError,
    UserSelfDeleteError,
)
from src.repositories.exceptions import (
    DepartmentIsUsingError,
    DepartmentNameAlreadyExistsError,
    DoctorDepartmentNotExistsError,
    DoctorInspectionNotExistsError,
    DoctorInvalidExpirienctStartError,
    DoctorSpecialityNotExistsError,
    EquipmentNameAlreadyExistsError,
    EquipmentTypeIsUsingError,
    EquipmentTypeNameAlreadyExistsError,
    EquipmentTypeNotExistsError,
    InspectionDoctorNotExistsError,
    InspectionTitleAlreadyExistsError,
    InspectionWasDeletedError,
    SpecialityIsUsingError,
    SpecialityNameAlreadyExistsError,
    UserEmailIsUsingError,
)
from src.services.exceptions import (
    EmptyPatchError,
    InvalidFileExtensionError,
    LoginError,
    NotFoundError,
    UnauthenticatedError,
)
from src.utils.exceptions import InvalidTokenSchemaError


def add_exception_handlers(app: FastAPI):
    @app.exception_handler(Exception)
    def handle_unexpected_err(request: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "detail": "Непредвиденная ошибка.",
            },
        )

    @app.exception_handler(NotFoundError)
    def handle_not_found(request: Request, exc: NotFoundError):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Страница не найдена."},
        )

    @app.exception_handler(UnauthenticatedError)
    def handle_authentication(request: Request, exc: UnauthenticatedError):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Unauthorized."},
        )

    @app.exception_handler(LoginError)
    def handle_login(request: Request, exc: LoginError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Неверный логин или пароль."},
        )

    @app.exception_handler(UserEmailIsUsingError)
    def handle_user_email_using(request: Request, exc: UserEmailIsUsingError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Пользователь с указанным email уже существует."},
        )

    @app.exception_handler(SpecialityNameAlreadyExistsError)
    def handle_speciality_exists(
        request: Request, exc: SpecialityNameAlreadyExistsError
    ):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Специальность с таким названием уже сушествует."},
        )

    @app.exception_handler(SpecialityIsUsingError)
    def handle_speciality_using(request: Request, exc: SpecialityIsUsingError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "detail": "Вы не можете изменить/удалить используемую специальность."
            },
        )

    @app.exception_handler(DepartmentNameAlreadyExistsError)
    def handle_department_exists(
        request: Request, exc: DepartmentNameAlreadyExistsError
    ):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Специальность с таким названием уже сушествует."},
        )

    @app.exception_handler(DepartmentIsUsingError)
    def handle_department_using(request: Request, exc: DepartmentIsUsingError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "detail": "Вы не можете изменить/удалить используемую специальность."
            },
        )

    @app.exception_handler(InspectionTitleAlreadyExistsError)
    def handle_inspection_title_exists(
        request: Request, exc: InspectionTitleAlreadyExistsError
    ):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Обследование с таким названием уже существует."},
        )

    @app.exception_handler(InspectionDoctorNotExistsError)
    def handle_inspection_doctor_exists(
        request: Request, exc: InspectionDoctorNotExistsError
    ):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Врач, добавленный к обследованию не существует."},
        )

    @app.exception_handler(EquipmentNameAlreadyExistsError)
    def handle_equipment_name_exists(
        request: Request, exc: EquipmentNameAlreadyExistsError
    ):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Оборудование с таким названием уже существует."},
        )

    @app.exception_handler(EquipmentTypeNotExistsError)
    def handle_equipment_type_not_exists(
        request: Request, exc: EquipmentTypeNotExistsError
    ):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Указанный тип оборудования не существует."},
        )

    @app.exception_handler(EquipmentTypeNameAlreadyExistsError)
    def handle_equipment_type_name_exists(
        request: Request, exc: EquipmentTypeNameAlreadyExistsError
    ):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Тип оборудования с таким названием уже существует."},
        )

    @app.exception_handler(EquipmentTypeIsUsingError)
    def handle_equipment_type_using(request: Request, exc: EquipmentTypeIsUsingError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "detail": "Вы не можете изменить/удалить используемый тип оборудования."
            },
        )

    @app.exception_handler(DoctorInvalidExpirienctStartError)
    def handle_doctor_invalid_experience_start(
        request: Request, exc: EquipmentTypeIsUsingError
    ):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Год начала стажа некорректен."},
        )

    @app.exception_handler(DoctorSpecialityNotExistsError)
    def handle_doctor_speciality_not_exists(
        request: Request, exc: DoctorSpecialityNotExistsError
    ):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "detail": "Выбраная специальность больше не существует, пожалуйста обновите страницу."
            },
        )

    @app.exception_handler(DoctorDepartmentNotExistsError)
    def handle_doctor_department_not_exists(
        request: Request, exc: DoctorSpecialityNotExistsError
    ):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "detail": "Выбраное отделение больше не существует, пожалуйста обновите страницу."
            },
        )

    @app.exception_handler(DoctorInspectionNotExistsError)
    def handle_doctor_inspection_not_exists(
        request: Request, exc: DoctorSpecialityNotExistsError
    ):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "detail": "Выбраное обследование больше не существует, пожалуйста обновите страницу."
            },
        )

    @app.exception_handler(InspectionWasDeletedError)
    def handle_inspection_create_error(
        request: Request, exc: InspectionWasDeletedError
    ):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Ошибка сохранения данных."},
        )

    @app.exception_handler(InvalidTokenSchemaError)
    def handle_invalid_token_create(request: Request, exc: InvalidTokenSchemaError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Ошибка создания токена авторизации."},
        )

    @app.exception_handler(InvalidFileExtensionError)
    def handle_invalid_file_ext(request: Request, exc: InvalidFileExtensionError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Недопустимый формат файла."},
        )

    @app.exception_handler(EmptyPatchError)
    def handle_empty_patch(request: Request, exc: EmptyPatchError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Ошибка обновления. Nothing to update."},
        )

    @app.exception_handler(PermissionError)
    def handle_permissions(request: Request, exc: PermissionError):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": "forbiden."},
        )

    @app.exception_handler(IssuedExcessUserPermissionsError)
    def handle_excess_users_permission(
        request: Request, exc: IssuedExcessUserPermissionsError
    ):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": "Вы не можете выдать права, превышающие ваши."},
        )

    @app.exception_handler(UserSelfDeleteError)
    def handle_self_delete(request: Request, exc: UserSelfDeleteError):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": "Вы не можете удалить свой аккаунт."},
        )
