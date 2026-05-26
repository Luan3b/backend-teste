from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.client import Client
from app.schemas.client_schema import ClientCreate

class ClientRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> Optional[Client]:
        return (
            self.db.query(Client)
            .filter(Client.cliente_email == email)
            .first()
        )

    def get_by_id(self, client_id: int) -> Optional[Client]:
        return (
            self.db.query(Client)
            .filter(Client.id == client_id)
            .first()
        )

    def create(self, client_in: ClientCreate) -> Client:
        client = Client(
            **client_in.model_dump(),
            status="Aguardando Análise"
        )

        self.db.add(client)

        try:
            self.db.commit()
            self.db.refresh(client)

        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

        return client

    def update_status_and_priority(
        self,
        client_id: int,
        status: str,
        prioridade: str
    ) -> Optional[Client]:

        client = self.get_by_id(client_id)

        if not client:
            return None

        client.status = status
        client.prioridade = prioridade

        try:
            self.db.commit()
            self.db.refresh(client)

        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

        return client