from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from app.repositories.client_repository import ClientRepository
from app.repositories.webhook_repository import WebhookRepository
from app.schemas.webhook_schema import WebhookPayload
from app.services.pipefy_service import PipefyService

STATUS_PROCESSADO = "Processado"

PRIORIDADE_ALTA = "prioridade_alta"
PRIORIDADE_NORMAL = "prioridade_normal"

class WebhookService:
    def __init__(self, webhook_repo: WebhookRepository, client_repo: ClientRepository, pipefy_service: PipefyService):
        self.webhook_repo = webhook_repo
        self.client_repo = client_repo
        self.pipefy_service = pipefy_service

    def processar_update_card(
        self,
        payload: WebhookPayload
    ):

        try:
            self.webhook_repo.save_event(payload)

        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Evento já processado (Idempotência ativa)."
            )

        cliente = self.client_repo.get_by_email(
            payload.cliente_email
        )

        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente não encontrado."
            )

        prioridade = (
            PRIORIDADE_ALTA
            if cliente.valor_patrimonio >= 200000
            else PRIORIDADE_NORMAL
        )

        self.pipefy_service.simulate_update_card_field(
            card_id=payload.card_id,
            status=STATUS_PROCESSADO,
            prioridade=prioridade
        )

        self.client_repo.update_status_and_priority(
            cliente.id,
            STATUS_PROCESSADO,
            prioridade
        )

        return {
            "status": "sucesso",
            "cliente_email": cliente.cliente_email,
            "prioridade_definida": prioridade
        }