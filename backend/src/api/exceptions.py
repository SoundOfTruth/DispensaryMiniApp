class ServiceException(Exception):
    pass


class NotFoundException(ServiceException):
    pass

class DbIntegrityException(ServiceException):
    def __init__(self, detail: str):
        self.detail = detail
