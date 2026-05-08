class RepositoryError(Exception):
    pass


class UserEmailIsUsingError(RepositoryError):
    pass


class SpecialityNameAlreadyExistsError(RepositoryError):
    pass


class SpecialityIsUsingError(RepositoryError):
    pass


class DepartmentNameAlreadyExistsError(RepositoryError):
    pass


class DepartmentIsUsingError(RepositoryError):
    pass


class EquipmentNameAlreadyExistsError(RepositoryError):
    pass


class EquipmentTypeNotExistsError(RepositoryError):
    pass


class EquipmentTypeNameAlreadyExistsError(RepositoryError):
    pass


class EquipmentTypeIsUsingError(RepositoryError):
    pass


class InspectionTitleAlreadyExistsError(RepositoryError):
    pass


class InspectionDoctorNotExistsError(RepositoryError):
    pass


class InspectionWasDeletedError(RepositoryError):
    pass


class DoctorInvalidExpirienctStartError(RepositoryError):
    pass


class DoctorSpecialityNotExistsError(RepositoryError):
    pass


class DoctorDepartmentNotExistsError(RepositoryError):
    pass


class DoctorInspectionNotExistsError(RepositoryError):
    pass


class DoctorWasDeletedError(RepositoryError):
    pass
