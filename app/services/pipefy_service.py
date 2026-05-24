import logging
from typing import Dict, Any

logger = logging.getLogger("uvicorn")


class PipefyService:
    """
    Camada de Serviço responsável por mapear as integrações com o Pipefy.
    Contém a sintaxe rigorosa exigida pela especificação GraphQL v2 oficial do Pipefy.
    """

    def simulate_create_card(self, nome: str, email: str, patrimonio: float) -> Dict[str, Any]:
        # Sintaxe real baseada na documentação pública do Pipefy
        query = """
        mutation CreateClientCard($input: CreateCardInput!) {
          createCard(input: $input) {
            card {
              id
              title
            }
          }
        }
        """

        # Variáveis estruturadas simulando o envio real.
        # No Pipefy, dados customizados populam a propriedade 'fields_attributes'
        variables = {
            "input": {
                "pipe_id": "301548291",  # ID fictício do Pipe (esteira de processos)
                "title": f"Análise Patrimonial - {nome}",
                "fields_attributes": [
                    {"field_id": "email_do_cliente", "field_value": email},
                    {"field_id": "patrimonio_investido", "field_value": str(patrimonio)},
                    {"field_id": "status_analise", "field_value": "Aguardando Análise"}
                ]
            }
        }

        # Exibe no terminal o payload idêntico ao que iria para a produção
        logger.info("[Pipefy GraphQL] Executando Mutation: createCard")
        logger.info(f"[Pipefy GraphQL] Query String: {query}")
        logger.info(f"[Pipefy GraphQL] Variables Payload: {variables}")

        return {"query": query, "variables": variables}

    def simulate_update_card_field(self, card_id: str, status: str, prioridade: str) -> Dict[str, Any]:
        # Nota de busca na Doc: Para alterar propriedades customizadas de um card,
        # o Pipefy adota a mutation 'updateCardField' que manipula um campo por vez.
        query = """
        mutation UpdateClientCardField($input: UpdateCardFieldInput!) {
          updateCardField(input: $input) {
            card {
              id
            }
          }
        }
        """

        # Simulação alterando o campo customizado que mapeia a prioridade calculada
        variables = {
            "input": {
                "card_id": card_id,
                "field_id": "prioridade_analise",
                "values": [prioridade]
            }
        }

        logger.info("[Pipefy GraphQL] Executando Mutation: updateCardField")
        logger.info(f"[Pipefy GraphQL] Query String: {query}")
        logger.info(f"[Pipefy GraphQL] Variables Payload: {variables}")

        return {"query": query, "variables": variables}