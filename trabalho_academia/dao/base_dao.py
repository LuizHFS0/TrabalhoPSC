from __future__ import annotations

from typing import Generic, Optional, Type, TypeVar

from sqlalchemy.orm import Session

from database.base import Base

T = TypeVar("T", bound=Base)


class BaseDAO(Generic[T]):
    """
    DAO genérico com operações CRUD básicas.
    Regra: DAO apenas acessa o banco — sem lógica de negócio.
    """

    def __init__(self, model: Type[T], session: Session) -> None:
        self._model = model
        self._session = session

    def create(self, obj: T) -> T:
        self._session.add(obj)
        self._session.flush()
        self._session.refresh(obj)
        return obj

    def get_by_id(self, id: int) -> Optional[T]:
        return self._session.get(self._model, id)

    def get_all(self) -> list[T]:
        return list(self._session.query(self._model).all())

    def update(self, obj: T) -> T:
        self._session.flush()
        self._session.refresh(obj)
        return obj

    def delete(self, obj: T) -> None:
        self._session.delete(obj)
        self._session.flush()
