from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from dao.base_dao import BaseDAO
from database.models import Usuario


class UsuarioDAO(BaseDAO[Usuario]):

    def __init__(self, session: Session) -> None:
        super().__init__(Usuario, session)

    def buscar_por_usuario(self, usuario: str) -> Optional[Usuario]:
        return (
            self._session.query(Usuario)
            .filter(Usuario.usuario == usuario)
            .first()
        )

    def buscar_por_email(self, email: str) -> Optional[Usuario]:
        return (
            self._session.query(Usuario)
            .filter(Usuario.email == email)
            .first()
        )

    def buscar_por_cpf(self, cpf: str) -> Optional[Usuario]:
        return (
            self._session.query(Usuario)
            .filter(Usuario.cpf == cpf)
            .first()
        )
