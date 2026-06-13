import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.base import Base
from database.models import Usuario, PerfilFisico, Treino  # noqa: F401
from services.usuario_service import UsuarioService
from services.auth_service import AuthService
from utils.exceptions import (
    CPFJaExisteError,
    EmailJaExisteError,
    LoginInvalidoError,
    UsuarioJaExisteError,
)


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, autocommit=False, autoflush=False, expire_on_commit=False)
    s = Session()
    yield s
    s.close()
    Base.metadata.drop_all(engine)


def _dados_base(**override):
    dados = dict(
        nome_completo="João Silva",
        cpf="529.982.247-25",
        email="joao@email.com",
        usuario="joaosilva",
        senha="Senha@123",
    )
    dados.update(override)
    return dados


# ── Cadastro ──────────────────────────────────────────────────────────

def test_cadastrar_usuario_sucesso(session):
    svc = UsuarioService(session)
    u = svc.cadastrar(**_dados_base())
    assert u.id is not None
    assert u.usuario == "joaosilva"


def test_cadastrar_cpf_duplicado(session):
    svc = UsuarioService(session)
    svc.cadastrar(**_dados_base())
    with pytest.raises(CPFJaExisteError):
        svc.cadastrar(**_dados_base(usuario="outro", email="outro@email.com"))


def test_cadastrar_email_duplicado(session):
    svc = UsuarioService(session)
    svc.cadastrar(**_dados_base())
    with pytest.raises(EmailJaExisteError):
        svc.cadastrar(**_dados_base(usuario="outro", cpf="111.444.777-35"))


def test_cadastrar_usuario_duplicado(session):
    svc = UsuarioService(session)
    svc.cadastrar(**_dados_base())
    with pytest.raises(UsuarioJaExisteError):
        svc.cadastrar(**_dados_base(cpf="111.444.777-35", email="novo@email.com"))


def test_cadastrar_cpf_invalido(session):
    svc = UsuarioService(session)
    with pytest.raises(ValueError):
        svc.cadastrar(**_dados_base(cpf="000.000.000-00"))


def test_cadastrar_email_invalido(session):
    svc = UsuarioService(session)
    with pytest.raises(ValueError):
        svc.cadastrar(**_dados_base(email="nao-e-email"))


# ── Login ─────────────────────────────────────────────────────────────

def test_login_sucesso(session):
    UsuarioService(session).cadastrar(**_dados_base())
    session.commit()
    u = AuthService(session).autenticar("joaosilva", "Senha@123")
    assert u.usuario == "joaosilva"


def test_login_senha_errada(session):
    UsuarioService(session).cadastrar(**_dados_base())
    session.commit()
    with pytest.raises(LoginInvalidoError):
        AuthService(session).autenticar("joaosilva", "senhaErrada")


def test_login_usuario_inexistente(session):
    with pytest.raises(LoginInvalidoError):
        AuthService(session).autenticar("ninguem", "qualquer")


# ── Alteração de senha ────────────────────────────────────────────────

def test_alterar_senha(session):
    UsuarioService(session).cadastrar(**_dados_base())
    session.commit()
    auth = AuthService(session)
    auth.alterar_senha("joaosilva", "Senha@123", "NovaSenha@456")
    session.commit()
    u = auth.autenticar("joaosilva", "NovaSenha@456")
    assert u is not None


def test_alterar_senha_atual_errada(session):
    UsuarioService(session).cadastrar(**_dados_base())
    session.commit()
    with pytest.raises(LoginInvalidoError):
        AuthService(session).alterar_senha("joaosilva", "SenhaErrada", "Nova@456")
