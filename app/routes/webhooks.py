from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.client_repository import ClientRepository
from app.repositories.webhook_repository import WebhookRepository
from app.schemas.webhook_schema import WebhookPayload
from app.services.webhook_service import WebhookService

router = APIRouter(prefix="/webhooks", tags=["Webhooks"])


# Mantemos o status 200 OK padrão para recebimento de webhooks processados com sucesso
@router.post("/pipefy/card-updated", status_code=status.HTTP_200_OK)
def card_updated_webhook_endpoint(payload: WebhookPayload, db: Session = Depends(get_db)):
    # 1. Instanciamos os repositórios necessários repassando a sessão do banco
    webhook_repo = WebhookRepository(db)
    client_repo = ClientRepository(db)
    
    # 2. Injetamos os repositórios no construtor do serviço correspondente
    service = WebhookService(webhook_repo=webhook_repo, client_repo=client_repo)
    
    # 3. Executamos a orquestração e retornamos o dicionário de sucesso do serviço
    return service.processar_update_card(payload)