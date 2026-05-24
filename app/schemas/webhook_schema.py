from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class WebhookPayload(BaseModel):
    event_id: str = Field(..., description="ID único do evento para controle de idempotência")
    card_id: str = Field(..., description="ID do card no Pipefy")
    cliente_email: EmailStr = Field(..., description="E-mail do cliente associado ao card")
    timestamp: datetime = Field(..., description="Timestamp do momento do evento no Pipefy")