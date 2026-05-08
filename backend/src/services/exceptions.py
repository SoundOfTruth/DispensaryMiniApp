class ServiceError(Exception):
    pass


class NotFoundError(ServiceError):
    pass


class UnauthenticatedError(ServiceError):
    pass


class UnauthorizedError(ServiceError):
    pass


class LoginError(ServiceError):
    pass


class InvalidPasswordError(ServiceError):
    pass


class InvalidFileExtensionError(ServiceError):
    pass


class EmptyPatchError(ServiceError):
    pass
