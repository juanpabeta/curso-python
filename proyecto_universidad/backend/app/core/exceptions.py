class AppError(Exception):
    """Excepción base para errores controlados de la aplicación."""

    def __init__(self, message: str, status_code: int = 400) -> None:
        self.message = message
        self.status_code = status_code


class NotFoundError(AppError):
    """Se lanza cuando un registro no existe."""

    def __init__(self, message: str) -> None:
        super().__init__(message, status_code=404)


class ValidationError(AppError):
    """Se lanza cuando la validación de la entidad falla."""

    def __init__(self, message: str) -> None:
        super().__init__(message, status_code=422)


class DuplicateError(AppError):
    """Se lanza cuando el valor a registrar ya existe."""

    def __init__(self, message: str) -> None:
        super().__init__(message, status_code=409)


class UnauthorizedError(AppError):
    """Se lanza cuando la autenticación o autorización falla."""

    def __init__(self, message: str) -> None:
        super().__init__(message, status_code=401)

class IntegrityConflictError(AppError):
    """Se lanza cuando no se puede eliminar un registro porque tiene dependencias."""

    def __init__(self, message: str) -> None:
        super().__init__(message, status_code=409)