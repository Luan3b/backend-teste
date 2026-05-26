from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field

class ClientCreate(BaseModel):
    cliente_nome: str = Field(..., min_length=2)
    cliente_email: EmailStr
    tipo_solicitacao: str
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

    model_config = ConfigDict(from_attributes=True)