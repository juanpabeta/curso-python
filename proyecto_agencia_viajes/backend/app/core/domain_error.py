class AppError(Exception):
    status_code = 400


class NotFoundError(AppError):
    status_code = 404


class DuplicateError(AppError):
    status_code = 409


class UnauthorizedError(AppError):
    status_code = 401
