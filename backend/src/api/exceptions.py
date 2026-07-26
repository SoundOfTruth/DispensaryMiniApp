class ApiError(Exception):
    pass


class InsufficientPermissionsError(ApiError):
    pass


class IssuedExcessUserPermissionsError(ApiError):
    pass


class UserSelfDeleteError(ApiError):
    pass


class UpdateSelfPasswordError(ApiError):
    pass
