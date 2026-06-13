import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.base import Base
from database.models import Usuario, PerfilFisico, Treino  # noqa: F401
from services.usuario_service import UsuarioService
from services.perfil_service import PerfilService
from utils.exceptions import PerfilNaoEncontradoError


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, autocommit=False, autoflush=False, expire_on_commit=False)
    s = Session()
    yield s
    s.close()
    Base.metadata.drop_all(engine)


@pytest.fixture
def usuario_id(session):
    u = UsuarioService(session).cadastrar(
        nome_completo="Maria Souza",
        cpf="529.982.247-25",
        email="maria@email.com",
        usuario="mariafit",
        senha="Senha@123",
    )
    session.commit()
    return u.id


def test_cadastrar_perfil_sucesso(session, usuario_id):
    svc = PerfilService(session)
    perfil = svc.cadastrar_perfil(usuario_id, idade=28, peso=65.0, altura=168.0, sexo="F")
    assert perfil.id is not None
    assert perfil.peso == 65.0


def test_buscar_perfil(session, usuario_id):
    svc = PerfilService(session)
    svc.cadastrar_perfil(usuario_id, idade=28, peso=65.0, altura=168.0)
    session.commit()
    perfil = svc.buscar_perfil(usuario_id)
    assert perfil.usuario_id == usuario_id


def test_perfil_nao_encontrado(session, usuario_id):
    with pytest.raises(PerfilNaoEncontradoError):
        PerfilService(session).buscar_perfil(usuario_id)


def test_atualizar_perfil(session, usuario_id):
    svc = PerfilService(session)
    svc.cadastrar_perfil(usuario_id, idade=28, peso=65.0, altura=168.0)
    session.commit()
    perfil = svc.atualizar_perfil(usuario_id, peso=63.5)
    assert perfil.peso == 63.5


def test_peso_invalido(session, usuario_id):
    with pytest.raises(ValueError):
        PerfilService(session).cadastrar_perfil(usuario_id, idade=28, peso=-5.0, altura=168.0)


def test_altura_invalida(session, usuario_id):
    with pytest.raises(ValueError):
        PerfilService(session).cadastrar_perfil(usuario_id, idade=28, peso=65.0, altura=0.0)


def test_idade_invalida(session, usuario_id):
    with pytest.raises(ValueError):
        PerfilService(session).cadastrar_perfil(usuario_id, idade=0, peso=65.0, altura=168.0)
