from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories.client_repository import ClientRepository
from app.schemas.client_schema import ClientCreate, ClientResponse
from app.services.client_service import ClientService
from app.services.pipefy_service import PipefyService

router = APIRouter(prefix="/clientes", tags=["Clientes"])

@router.post("", status_code=status.HTTP_201_CREATED, response_model=ClientResponse)
def create_client_endpoint(payload: ClientCreate, db: Session = Depends(get_db)):

    repo = ClientRepository(db)
    pipefy_service = PipefyService()
    
    service = ClientService(client_repo=repo, pipefy_service=pipefy_service)
    
    return service.registrar_cliente(payload)