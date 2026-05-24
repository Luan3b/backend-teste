from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.client_repository import ClientRepository
from app.schemas.client_schema import ClientCreate, ClientResponse
from app.services.client_service import ClientService

router = APIRouter(prefix="/clientes", tags=["Clientes"])


# Definimos status_code=201 (Created) para POSTs bem-sucedidos
# Injetamos o ClientResponse como contrato de saída oficial do endpoint
@router.post("", status_code=status.HTTP_201_CREATED, response_model=ClientResponse)
def create_client_endpoint(payload: ClientCreate, db: Session = Depends(get_db)):
    # 1. Instanciamos o repositório injetando a sessão do banco
    repo = ClientRepository(db)
    
    # 2. Injetamos o repositório criado no serviço correspondente
    service = ClientService(repo)
    
    # 3. Executamos a regra de negócio
    return service.registrar_cliente(payload)