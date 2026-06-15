from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from typing import Generator

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session, sessionmaker

from database.base import Base
from database.models import Usuario, PerfilFisico, Treino  # noqa: F401

_DB_PATH = Path(__file__).resolve().parent.parent / "treino.db"
_DB_URL = f"sqlite:///{_DB_PATH}"


class DatabaseManager:
    """Gerencia conexão, sessão e criação de tabelas."""

    def __init__(self, db_url: str = _DB_URL) -> None:
        self._engine: Engine = create_engine(
            db_url,
            echo=False,
            connect_args={"check_same_thread": False},
        )
        self._SessionFactory: sessionmaker[Session] = sessionmaker(
            bind=self._engine,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
        )

    def create_tables(self) -> None:
        Base.metadata.create_all(bind=self._engine)

    def drop_tables(self) -> None:
        Base.metadata.drop_all(bind=self._engine)

    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        session: Session = self._SessionFactory()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def get_raw_session(self) -> Session:
        return self._SessionFactory()

    @property
    def engine(self) -> Engine:
        return self._engine


db_manager = DatabaseManager()
