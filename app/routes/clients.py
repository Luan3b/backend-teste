from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.client_repository import ClientRepository
from app.schemas.client_schema import ClientCreate, ClientResponse
from app.services.client_service import ClientService
from app.services.pipefy_service import PipefyService

router = APIRouter(prefix="/clientes", tags=["Clientes"])


# Definimos status_code=201 (Created) para POSTs bem-sucedidos
# Injetamos o ClientResponse como contrato de saída oficial do endpoint
@router.post("", status_code=status.HTTP_201_CREATED, response_model=ClientResponse)
def create_client_endpoint(payload: ClientCreate, db: Session = Depends(get_db)):
    # 1. Instancia os adaptadores de Infraestrutura
    repo = ClientRepository(db)
    pipefy_service = PipefyService()
    
    # 2. Injeta os adaptadores no Core de Negócio (Service)
    service = ClientService(client_repo=repo, pipefy_service=pipefy_service)
    
    # 3. Executa a ação
    return service.registrar_cliente(payload)