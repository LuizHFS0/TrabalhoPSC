import re


def validar_email(email: str) -> bool:
    """Valida formato básico de e-mail."""
    pattern = r"^[\w\.\+\-]+@[\w\-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email.strip()))


def validar_cpf(cpf: str) -> bool:
    """
    Valida CPF (aceita formato 000.000.000-00 ou apenas dígitos).
    Verifica dígitos verificadores.
    """
    numeros = re.sub(r"\D", "", cpf)
    if len(numeros) != 11 or len(set(numeros)) == 1:
        return False

    def calcular_digito(parcial: str, pesos: list[int]) -> int:
        soma = sum(int(d) * p for d, p in zip(parcial, pesos))
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto

    d1 = calcular_digito(numeros[:9], list(range(10, 1, -1)))
    d2 = calcular_digito(numeros[:10], list(range(11, 1, -1)))
    return numeros[-2:] == f"{d1}{d2}"


def validar_telefone(telefone: str) -> bool:
    """Valida telefone brasileiro (8 a 11 dígitos, opcional DDD)."""
    numeros = re.sub(r"\D", "", telefone)
    return 8 <= len(numeros) <= 11


def validar_peso(peso: float) -> bool:
    """Peso deve ser maior que 0 e menor que 600 kg."""
    return 0 < peso < 600


def validar_altura(altura: float) -> bool:
    """Altura em cm — deve estar entre 30 e 300."""
    return 30 < altura < 300


def validar_idade(idade: int) -> bool:
    """Idade deve ser maior que 0 e menor que 130."""
    return 0 < idade < 130
