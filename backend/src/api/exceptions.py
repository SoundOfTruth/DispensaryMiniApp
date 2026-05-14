class ApiError(Exception):
    pass


class PermissionError(ApiError):
    pass


class IssuedExcessUserPermissionsError(ApiError):
    pass


class UserSelfDeleteError(ApiError):
    pass
