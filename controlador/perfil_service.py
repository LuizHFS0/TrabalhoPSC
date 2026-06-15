from __future__ import annotations

from sqlalchemy.orm import Session

from dao.perfil_dao import PerfilDAO
from database.models import PerfilFisico
from utils.exceptions import PerfilNaoEncontradoError
from utils.validators import validar_altura, validar_idade, validar_peso


class PerfilService:
    """Cadastro e atualização do perfil físico do usuário."""

    def __init__(self, session: Session) -> None:
        self._dao = PerfilDAO(session)

    def _validar_dados(self, peso: float, altura: float, idade: int) -> None:
        if not validar_peso(peso):
            raise ValueError(f"Peso inválido: {peso}. Deve ser entre 0 e 600 kg.")
        if not validar_altura(altura):
            raise ValueError(f"Altura inválida: {altura}. Deve ser entre 30 e 300 cm.")
        if not validar_idade(idade):
            raise ValueError(f"Idade inválida: {idade}. Deve ser entre 1 e 129 anos.")

    def cadastrar_perfil(
        self,
        usuario_id: int,
        idade: int,
        peso: float,
        altura: float,
        **kwargs,
    ) -> PerfilFisico:
        self._validar_dados(peso, altura, idade)
        existente = self._dao.buscar_por_usuario(usuario_id)
        if existente:
            raise ValueError(f"Usuário id={usuario_id} já possui perfil cadastrado.")

        perfil = PerfilFisico(
            usuario_id=usuario_id,
            idade=idade,
            peso=peso,
            altura=altura,
            **kwargs,
        )
        return self._dao.create(perfil)

    def atualizar_perfil(self, usuario_id: int, **campos) -> PerfilFisico:
        perfil = self._dao.buscar_por_usuario(usuario_id)
        if not perfil:
            raise PerfilNaoEncontradoError(f"Perfil do usuário id={usuario_id} não encontrado.")

        if "peso" in campos:
            if not validar_peso(campos["peso"]):
                raise ValueError(f"Peso inválido: {campos['peso']}.")
        if "altura" in campos:
            if not validar_altura(campos["altura"]):
                raise ValueError(f"Altura inválida: {campos['altura']}.")
        if "idade" in campos:
            if not validar_idade(campos["idade"]):
                raise ValueError(f"Idade inválida: {campos['idade']}.")

        for campo, valor in campos.items():
            setattr(perfil, campo, valor)
        return self._dao.update(perfil)

    def buscar_perfil(self, usuario_id: int) -> PerfilFisico:
        perfil = self._dao.buscar_por_usuario(usuario_id)
        if not perfil:
            raise PerfilNaoEncontradoError(f"Perfil do usuário id={usuario_id} não encontrado.")
        return perfil
