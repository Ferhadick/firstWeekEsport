from __future__ import annotations


class AppException(Exception):
    def __init__(self, message: str, details: str | None = None) -> None:
        self.message = message
        self.details = details
        super().__init__(message)


class NotFoundException(AppException):
    pass


class AlreadyExistsException(AppException):
    pass


class BusinessValidationException(AppException):
    pass


class DatabaseException(AppException):
    pass
