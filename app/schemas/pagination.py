"""Shared pagination and sorting DTOs."""

from __future__ import annotations

from typing import Generic, TypeVar

from pydantic import BaseModel

from app.exceptions import BusinessValidationException

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response wrapper."""

    items: list[T]
    page: int
    size: int
    total: int
    pages: int


def validate_sort_params(
    sort_by: str | None,
    order: str | None,
    valid_columns: set[str],
) -> None:
    """Validate sort_by column and order direction."""
    if sort_by and sort_by not in valid_columns:
        raise BusinessValidationException(
            f"Invalid sort column '{sort_by}'. "
            f"Valid columns: {', '.join(sorted(valid_columns))}"
        )
    if order and order not in ("asc", "desc"):
        raise BusinessValidationException(
            f"Invalid sort order '{order}'. Must be 'asc' or 'desc'."
        )
