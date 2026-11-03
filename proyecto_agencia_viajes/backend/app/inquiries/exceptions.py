from app.core.domain_error import NotFoundError, AppError


class InquiryNotFound(NotFoundError):
    pass


class InvalidStageTransition(AppError):
    pass
