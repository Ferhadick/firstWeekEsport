from __future__ import annotations

from typing import Generic, TypeVar

from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

from app.core.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    model: type[ModelType]

    def __init__(self, db: Session) -> None:
        self._db = db

    def get(self, id: int) -> ModelType | None:
        return self._db.query(self.model).filter(self.model.id == id).first()

    def get_all(
        self,
        *,
        page: int = 1,
        size: int = 10,
        sort_by: str | None = None,
        order: str | None = None,
    ) -> tuple[list[ModelType], int]:
        query = self._db.query(self.model)
        if sort_by:
            sort_column = getattr(self.model, sort_by)
            order_fn = asc if order == "asc" else desc
            query = query.order_by(order_fn(sort_column))
        total = query.count()
        items = query.offset((page - 1) * size).limit(size).all()
        return items, total

    def create(self, data: dict) -> ModelType:
        obj = self.model(**data)
        self._db.add(obj)
        self._db.commit()
        self._db.refresh(obj)
        return obj

    def update(self, obj: ModelType, updates: dict) -> ModelType:
        for key, value in updates.items():
            if value is not None:
                setattr(obj, key, value)
        self._db.commit()
        self._db.refresh(obj)
        return obj

    def delete(self, obj: ModelType) -> None:
        self._db.delete(obj)
        self._db.commit()
