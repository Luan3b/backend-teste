from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ClientCreate(BaseModel):
    # Field(..., min_length=2) garante que o nome não venha vazio ou com uma letra só
    cliente_nome: str = Field(..., min_length=2)
    cliente_email: EmailStr
    tipo_solicitacao: str
    # ge=0 impede que enviem patrimônio negativo por acidente
    valor_patrimonio: float = Field(..., ge=0)


class ClientResponse(BaseModel):
    id: int
    cliente_nome: str
    cliente_email: str
    tipo_solicitacao: str
    valor_patrimonio: float
    status: str
    prioridade: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    # Padrão moderno de configuração do Pydantic v2
    model_config = ConfigDict(from_attributes=True)