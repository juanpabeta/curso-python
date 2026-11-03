from app.core.domain_error import DuplicateError, NotFoundError


class UserAlreadyExists(DuplicateError):
    pass


class UserNotFound(NotFoundError):
    pass
