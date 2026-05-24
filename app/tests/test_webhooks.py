def test_webhook_prioridade_alta(client):

    # cria cliente
    client.post(
        "/clientes",
        json={
            "cliente_nome": "Maria",
            "cliente_email": "maria@email.com",
            "tipo_solicitacao": "Análise",
            "valor_patrimonio": 300000
        }
    )

    payload = {
        "event_id": "evt_001",
        "card_id": "card_001",
        "cliente_email": "maria@email.com",
        "timestamp": "2026-05-18T12:00:00Z"
    }

    response = client.post(
        "/webhooks/pipefy/card-updated",
        json=payload
    )

    assert response.status_code == 200

    body = response.json()

    assert body["prioridade_definida"] == "prioridade_alta"


def test_webhook_prioridade_normal(client):

    client.post(
        "/clientes",
        json={
            "cliente_nome": "Carlos",
            "cliente_email": "carlos@email.com",
            "tipo_solicitacao": "Análise",
            "valor_patrimonio": 100000
        }
    )

    payload = {
        "event_id": "evt_002",
        "card_id": "card_002",
        "cliente_email": "carlos@email.com",
        "timestamp": "2026-05-18T12:00:00Z"
    }

    response = client.post(
        "/webhooks/pipefy/card-updated",
        json=payload
    )

    assert response.status_code == 200

    body = response.json()

    assert body["prioridade_definida"] == "prioridade_normal"


def test_webhook_evento_duplicado(client):

    client.post(
        "/clientes",
        json={
            "cliente_nome": "Pedro",
            "cliente_email": "pedro@email.com",
            "tipo_solicitacao": "Análise",
            "valor_patrimonio": 500000
        }
    )

    payload = {
        "event_id": "evt_duplicate",
        "card_id": "card_003",
        "cliente_email": "pedro@email.com",
        "timestamp": "2026-05-18T12:00:00Z"
    }

    first_response = client.post(
        "/webhooks/pipefy/card-updated",
        json=payload
    )

    second_response = client.post(
        "/webhooks/pipefy/card-updated",
        json=payload
    )

    assert first_response.status_code == 200
    assert second_response.status_code == 409