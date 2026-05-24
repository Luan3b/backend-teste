import re
from enum import Enum


LIMITE_PRIORIDADE_ALTA = 200000


class PrioridadeEnum(str, Enum):
    ALTA = "prioridade_alta"
    NORMAL = "prioridade_normal"


def validar_email(email: str) -> bool:
    """
    Validação semântica de formato de e-mail.
    Camada secundária de validação além do Pydantic.
    """

    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    return bool(re.match(pattern, email))


def calcular_prioridade(
    valor_patrimonio: float
) -> PrioridadeEnum:
    """
    Regra de negócio centralizada para classificação
    de prioridade do cliente.
    """

    if valor_patrimonio >= LIMITE_PRIORIDADE_ALTA:
        return PrioridadeEnum.ALTA

    return PrioridadeEnum.NORMAL