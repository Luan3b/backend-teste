from fastapi import HTTPException, status

from app.models.client import Client
from app.repositories.client_repository import ClientRepository
from app.schemas.client_schema import ClientCreate
from app.services.pipefy_service import PipefyService


class ClientService:
    def __init__(self, client_repo: ClientRepository, pipefy_service: PipefyService):
        self.client_repo = client_repo
        self.pipefy_service = pipefy_service

    def registrar_cliente(
        self,
        client_in: ClientCreate
    ) -> Client:

        cliente_existente = self.client_repo.get_by_email(
            client_in.cliente_email
        )

        if cliente_existente:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="E-mail já cadastrado no sistema."
            )

        novo_cliente = self.client_repo.create(client_in)

        try:
            self.pipefy_service.simulate_create_card(
                nome=novo_cliente.cliente_nome,
                email=novo_cliente.cliente_email,
                patrimonio=novo_cliente.valor_patrimonio
            )

        except Exception as exc:
            print(f"Erro integração Pipefy: {exc}")

        return novo_cliente