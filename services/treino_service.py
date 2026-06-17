from __future__ import annotations

from sqlalchemy.orm import Session

from dao.treino_dao import TreinoDAO
from database.models import Treino
from utils.exceptions import TreinoNaoEncontradoError


class TreinoService:
    def __init__(self, session: Session) -> None:
        self._dao = TreinoDAO(session)
        self._session = session

    def criar_treino(
        self,
        usuario_id: int,
        nome_treino: str,
        exercicio: str,
        series: int,
        repeticoes: int,
        carga: float | None = None,
        observacoes: str | None = None,
    ) -> Treino:
        if series <= 0:
            raise ValueError("Séries deve ser maior que 0.")
        if repeticoes <= 0:
            raise ValueError("Repetições deve ser maior que 0.")

        treino = Treino(
            usuario_id=usuario_id,
            nome_treino=nome_treino,
            exercicio=exercicio,
            series=series,
            repeticoes=repeticoes,
            carga=carga,
            observacoes=observacoes,
        )
        try:
            resultado = self._dao.create(treino)
            self._session.commit()
            return resultado
        except Exception:
            self._session.rollback()
            raise

    def listar_treinos(self, usuario_id: int) -> list[Treino]:
        return self._dao.listar_por_usuario(usuario_id)

    def buscar_por_nome(self, usuario_id: int, nome: str) -> list[Treino]:
        return self._dao.buscar_por_nome(usuario_id, nome)

    def atualizar_treino(self, treino_id: int, **campos) -> Treino:
        treino = self._dao.get_by_id(treino_id)
        if not treino:
            raise TreinoNaoEncontradoError(f"Treino id={treino_id} não encontrado.")
        for campo, valor in campos.items():
            setattr(treino, campo, valor)
        return self._dao.update(treino)

    def excluir_treino(self, treino_id: int) -> None:
        treino = self._dao.get_by_id(treino_id)
        if not treino:
            raise TreinoNaoEncontradoError(f"Treino id={treino_id} não encontrado.")
        self._dao.delete(treino)