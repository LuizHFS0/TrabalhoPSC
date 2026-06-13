from __future__ import annotations

from sqlalchemy.orm import Session

from dao.base_dao import BaseDAO
from database.models import Treino


class TreinoDAO(BaseDAO[Treino]):

    def __init__(self, session: Session) -> None:
        super().__init__(Treino, session)

    def listar_por_usuario(self, usuario_id: int) -> list[Treino]:
        return (
            self._session.query(Treino)
            .filter(Treino.usuario_id == usuario_id)
            .order_by(Treino.data_criacao.desc())
            .all()
        )

    def buscar_por_nome(self, usuario_id: int, nome_treino: str) -> list[Treino]:
        return (
            self._session.query(Treino)
            .filter(
                Treino.usuario_id == usuario_id,
                Treino.nome_treino.ilike(f"%{nome_treino}%"),
            )
            .all()
        )
