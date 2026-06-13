from __future__ import annotations

from sqlalchemy.orm import Session

from dao.usuario_dao import UsuarioDAO
from database.models import Usuario
from utils.exceptions import LoginInvalidoError, UsuarioJaExisteError, UsuarioNaoEncontradoError
from utils.security import gerar_hash, verificar_senha
from utils.validators import validar_email


class AuthService:
    """Responsável por registro, login e alteração de senha."""

    def __init__(self, session: Session) -> None:
        self._session = session
        self._usuario_dao = UsuarioDAO(session)

    def registrar(
        self,
        nome_completo: str,
        cpf: str,
        email: str,
        usuario: str,
        senha: str,
        **kwargs,
    ) -> Usuario:
        if self._usuario_dao.buscar_por_usuario(usuario):
            raise UsuarioJaExisteError(f"Usuário '{usuario}' já existe.")

        novo = Usuario(
            nome_completo=nome_completo,
            cpf=cpf,
            email=email,
            usuario=usuario,
            senha_hash=gerar_hash(senha),
            **kwargs,
        )
        return self._usuario_dao.create(novo)

    def autenticar(self, usuario: str, senha: str) -> Usuario:
        obj = self._usuario_dao.buscar_por_usuario(usuario)
        if not obj or not verificar_senha(senha, obj.senha_hash):
            raise LoginInvalidoError("Usuário ou senha inválidos.")
        return obj

    def alterar_senha(self, usuario: str, senha_atual: str, nova_senha: str) -> None:
        obj = self.autenticar(usuario, senha_atual)
        obj.senha_hash = gerar_hash(nova_senha)
        self._usuario_dao.update(obj)
