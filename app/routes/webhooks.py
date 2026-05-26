from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories.client_repository import ClientRepository
from app.repositories.webhook_repository import WebhookRepository
from app.schemas.webhook_schema import WebhookPayload
from app.services.webhook_service import WebhookService
from app.services.pipefy_service import PipefyService

router = APIRouter(prefix="/webhooks", tags=["Webhooks"])


@router.post("/pipefy/card-updated", status_code=status.HTTP_200_OK)
def card_updated_webhook_endpoint(payload: WebhookPayload, db: Session = Depends(get_db)):

    webhook_repo = WebhookRepository(db)
    client_repo = ClientRepository(db)
    pipefy_service = PipefyService() 
    
    service = WebhookService(
        webhook_repo=webhook_repo, 
        client_repo=client_repo,
        pipefy_service=pipefy_service # 
    )
    
    return service.processar_update_card(payload)