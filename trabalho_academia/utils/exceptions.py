class UsuarioJaExisteError(Exception):
    """Lançada quando o nome de usuário já está cadastrado."""


class CPFJaExisteError(Exception):
    """Lançada quando o CPF já está cadastrado."""


class EmailJaExisteError(Exception):
    """Lançada quando o e-mail já está cadastrado."""


class LoginInvalidoError(Exception):
    """Lançada quando usuário ou senha estão incorretos."""


class PerfilNaoEncontradoError(Exception):
    """Lançada quando o perfil físico não é encontrado."""


class TreinoNaoEncontradoError(Exception):
    """Lançada quando o treino não é encontrado."""


class UsuarioNaoEncontradoError(Exception):
    """Lançada quando o usuário não é encontrado."""
