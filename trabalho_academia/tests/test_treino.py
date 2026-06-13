import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.base import Base
from database.models import Usuario, PerfilFisico, Treino  # noqa: F401
from services.usuario_service import UsuarioService
from services.treino_service import TreinoService
from utils.exceptions import TreinoNaoEncontradoError


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
        nome_completo="Pedro Costa",
        cpf="529.982.247-25",
        email="pedro@email.com",
        usuario="pedrofit",
        senha="Senha@123",
    )
    session.commit()
    return u.id


def _treino(usuario_id, **override):
    dados = dict(
        usuario_id=usuario_id,
        nome_treino="Treino A",
        exercicio="Supino Reto",
        series=4,
        repeticoes=10,
        carga=60.0,
    )
    dados.update(override)
    return dados


def test_criar_treino(session, usuario_id):
    svc = TreinoService(session)
    t = svc.criar_treino(**_treino(usuario_id))
    assert t.id is not None
    assert t.exercicio == "Supino Reto"


def test_listar_treinos(session, usuario_id):
    svc = TreinoService(session)
    svc.criar_treino(**_treino(usuario_id))
    svc.criar_treino(**_treino(usuario_id, exercicio="Agachamento", nome_treino="Treino B"))
    session.commit()
    treinos = svc.listar_treinos(usuario_id)
    assert len(treinos) == 2


def test_buscar_por_nome(session, usuario_id):
    svc = TreinoService(session)
    svc.criar_treino(**_treino(usuario_id, nome_treino="Treino A"))
    svc.criar_treino(**_treino(usuario_id, nome_treino="Treino B"))
    session.commit()
    resultado = svc.buscar_por_nome(usuario_id, "Treino A")
    assert len(resultado) == 1


def test_atualizar_treino(session, usuario_id):
    svc = TreinoService(session)
    t = svc.criar_treino(**_treino(usuario_id))
    session.commit()
    atualizado = svc.atualizar_treino(t.id, carga=80.0)
    assert atualizado.carga == 80.0


def test_excluir_treino(session, usuario_id):
    svc = TreinoService(session)
    t = svc.criar_treino(**_treino(usuario_id))
    session.commit()
    svc.excluir_treino(t.id)
    session.commit()
    with pytest.raises(TreinoNaoEncontradoError):
        svc.excluir_treino(t.id)


def test_series_invalidas(session, usuario_id):
    with pytest.raises(ValueError):
        TreinoService(session).criar_treino(**_treino(usuario_id, series=0))


def test_repeticoes_invalidas(session, usuario_id):
    with pytest.raises(ValueError):
        TreinoService(session).criar_treino(**_treino(usuario_id, repeticoes=-1))
