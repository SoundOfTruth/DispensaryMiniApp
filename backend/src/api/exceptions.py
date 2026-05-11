class ApiError(Exception):
    pass


class PermissionError(ApiError):
    pass

class IssuedExcessUserPermissions(ApiError):
    pass
