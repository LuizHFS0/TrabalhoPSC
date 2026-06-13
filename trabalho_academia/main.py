"""
trabalho_academia — menu de terminal para validação do backend.
Execute: python main.py
"""
from __future__ import annotations

import sys

from database.database import db_manager
from services.auth_service import AuthService
from services.perfil_service import PerfilService
from services.treino_service import TreinoService
from services.usuario_service import UsuarioService
from utils.exceptions import (
    CPFJaExisteError,
    EmailJaExisteError,
    LoginInvalidoError,
    PerfilNaoEncontradoError,
    TreinoNaoEncontradoError,
    UsuarioJaExisteError,
)

# Inicializa tabelas na primeira execução
db_manager.create_tables()

_usuario_logado = None  # Objeto Usuario da sessão atual


def _input(prompt: str) -> str:
    return input(prompt).strip()


# ── Ações ──────────────────────────────────────────────────────────────────────

def cadastrar_usuario():
    print("\n── Cadastrar Usuário ──")
    try:
        with db_manager.get_session() as s:
            svc = UsuarioService(s)
            u = svc.cadastrar(
                nome_completo=_input("Nome completo : "),
                cpf=_input("CPF           : "),
                email=_input("E-mail        : "),
                usuario=_input("Usuário       : "),
                senha=_input("Senha         : "),
                telefone=_input("Telefone      : ") or None,
            )
        print(f"✔ Usuário '{u.usuario}' cadastrado com id={u.id}.")
    except (CPFJaExisteError, EmailJaExisteError, UsuarioJaExisteError, ValueError) as e:
        print(f"✘ {e}")


def login():
    global _usuario_logado
    print("\n── Login ──")
    try:
        with db_manager.get_session() as s:
            u = AuthService(s).autenticar(
                _input("Usuário : "),
                _input("Senha   : "),
            )
        _usuario_logado = u
        print(f"✔ Bem-vindo, {u.nome_completo}!")
    except LoginInvalidoError as e:
        print(f"✘ {e}")


def _exige_login() -> bool:
    if not _usuario_logado:
        print("✘ Faça login primeiro (opção 2).")
        return False
    return True


def criar_perfil():
    if not _exige_login():
        return
    print("\n── Criar Perfil Físico ──")
    try:
        with db_manager.get_session() as s:
            p = PerfilService(s).cadastrar_perfil(
                usuario_id=_usuario_logado.id,
                idade=int(_input("Idade  : ")),
                peso=float(_input("Peso (kg) : ")),
                altura=float(_input("Altura (cm): ")),
                sexo=_input("Sexo (M/F/outro): ") or None,
                objetivo=_input("Objetivo : ") or None,
                nivel=_input("Nível (iniciante/intermediário/avançado): ") or None,
            )
        print(f"✔ Perfil criado com id={p.id}.")
    except (PerfilNaoEncontradoError, ValueError) as e:
        print(f"✘ {e}")


def criar_treino():
    if not _exige_login():
        return
    print("\n── Criar Treino ──")
    try:
        with db_manager.get_session() as s:
            t = TreinoService(s).criar_treino(
                usuario_id=_usuario_logado.id,
                nome_treino=_input("Nome do treino : "),
                exercicio=_input("Exercício      : "),
                series=int(_input("Séries         : ")),
                repeticoes=int(_input("Repetições     : ")),
                carga=float(_input("Carga (kg)     : ") or 0) or None,
                observacoes=_input("Observações    : ") or None,
            )
        print(f"✔ Treino '{t.nome_treino}' criado com id={t.id}.")
    except ValueError as e:
        print(f"✘ {e}")


def listar_treinos():
    if not _exige_login():
        return
    with db_manager.get_session() as s:
        treinos = TreinoService(s).listar_treinos(_usuario_logado.id)
    if not treinos:
        print("Nenhum treino cadastrado.")
        return
    print(f"\n── Treinos de {_usuario_logado.usuario} ──")
    for t in treinos:
        carga = f"{t.carga}kg" if t.carga else "—"
        print(f"  [{t.id}] {t.nome_treino} | {t.exercicio} | {t.series}x{t.repeticoes} | {carga}")


def alterar_senha():
    if not _exige_login():
        return
    print("\n── Alterar Senha ──")
    try:
        with db_manager.get_session() as s:
            AuthService(s).alterar_senha(
                _usuario_logado.usuario,
                _input("Senha atual : "),
                _input("Nova senha  : "),
            )
        print("✔ Senha alterada com sucesso.")
    except LoginInvalidoError as e:
        print(f"✘ {e}")


def excluir_treino():
    if not _exige_login():
        return
    listar_treinos()
    try:
        tid = int(_input("\nID do treino a excluir: "))
        with db_manager.get_session() as s:
            TreinoService(s).excluir_treino(tid)
        print(f"✔ Treino id={tid} excluído.")
    except (TreinoNaoEncontradoError, ValueError) as e:
        print(f"✘ {e}")


# ── Menu ───────────────────────────────────────────────────────────────────────

_MENU = """
╔══════════════════════════════╗
║      trabalho_academia       ║
╠══════════════════════════════╣
║  1 · Cadastrar usuário       ║
║  2 · Login                   ║
║  3 · Criar perfil físico     ║
║  4 · Criar treino            ║
║  5 · Listar treinos          ║
║  6 · Alterar senha           ║
║  7 · Excluir treino          ║
║  8 · Sair                    ║
╚══════════════════════════════╝
"""

_ACOES = {
    "1": cadastrar_usuario,
    "2": login,
    "3": criar_perfil,
    "4": criar_treino,
    "5": listar_treinos,
    "6": alterar_senha,
    "7": excluir_treino,
}

if __name__ == "__main__":
    while True:
        print(_MENU)
        if _usuario_logado:
            print(f"  Logado como: {_usuario_logado.usuario}\n")
        opcao = _input("Opção: ")
        if opcao == "8":
            print("Até mais!")
            sys.exit(0)
        acao = _ACOES.get(opcao)
        if acao:
            acao()
        else:
            print("Opção inválida.")
