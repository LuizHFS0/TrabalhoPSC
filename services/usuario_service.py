from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from dao.usuario_dao import UsuarioDAO
from database.models import Usuario
from utils.exceptions import (
    CPFJaExisteError,
    EmailJaExisteError,
    UsuarioJaExisteError,
    UsuarioNaoEncontradoError,
)
from utils.validators import validar_cpf, validar_email
from utils.security import gerar_hash


class UsuarioService:
    """CRUD de usuário com validação de unicidade."""

    def __init__(self, session: Session) -> None:
        self._dao = UsuarioDAO(session)

    def cadastrar(
        self,
        nome_completo: str,
        cpf: str,
        email: str,
        usuario: str,
        senha: str,
        **kwargs,
    ) -> Usuario:
        if not validar_cpf(cpf):
            raise ValueError(f"CPF inválido: {cpf}")
        if not validar_email(email):
            raise ValueError(f"E-mail inválido: {email}")
        if self._dao.buscar_por_cpf(cpf):
            raise CPFJaExisteError(f"CPF '{cpf}' já cadastrado.")
        if self._dao.buscar_por_email(email):
            raise EmailJaExisteError(f"E-mail '{email}' já cadastrado.")
        if self._dao.buscar_por_usuario(usuario):
            raise UsuarioJaExisteError(f"Usuário '{usuario}' já existe.")

        obj = Usuario(
            nome_completo=nome_completo,
            cpf=cpf,
            email=email,
            usuario=usuario,
            senha_hash=gerar_hash(senha),
            **kwargs,
        )
        return self._dao.create(obj)

    def buscar_por_id(self, id: int) -> Usuario:
        obj = self._dao.get_by_id(id)
        if not obj:
            raise UsuarioNaoEncontradoError(f"Usuário id={id} não encontrado.")
        return obj

    def atualizar(self, id: int, **campos) -> Usuario:
        obj = self.buscar_por_id(id)
        for campo, valor in campos.items():
            setattr(obj, campo, valor)
        return self._dao.update(obj)

    def excluir(self, id: int) -> None:
        obj = self.buscar_por_id(id)
        self._dao.delete(obj)

    def listar(self) -> list[Usuario]:
        return self._dao.get_all()
