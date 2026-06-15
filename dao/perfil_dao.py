from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from dao.base_dao import BaseDAO
from database.models import PerfilFisico


class PerfilDAO(BaseDAO[PerfilFisico]):

    def __init__(self, session: Session) -> None:
        super().__init__(PerfilFisico, session)

    def buscar_por_usuario(self, usuario_id: int) -> Optional[PerfilFisico]:
        return (
            self._session.query(PerfilFisico)
            .filter(PerfilFisico.usuario_id == usuario_id)
            .first()
        )
