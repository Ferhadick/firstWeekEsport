"""Custom exceptions for the application."""

from __future__ import annotations


class AppException(Exception):
    """Base exception for all application errors."""

    def __init__(self, message: str, details: str | None = None) -> None:
        self.message = message
        self.details = details
        super().__init__(message)


class NotFoundException(AppException):
    """Raised when a requested resource is not found."""


class AlreadyExistsException(AppException):
    """Raised when a resource with the given identifier already exists."""


class BusinessValidationException(AppException):
    """Raised when a business rule is violated."""


class DatabaseException(AppException):
    """Raised when a database error occurs."""
