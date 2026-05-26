def test_webhook_prioridade_alta(client):

    client.post(
        "/clientes",
        json={
            "cliente_nome": "sonia",
            "cliente_email": "sonia@email.com",
            "tipo_solicitacao": "Análise",
            "valor_patrimonio": 300000
        }
    )

    payload = {
        "event_id": "evt_001",
        "card_id": "card_001",
        "cliente_email": "sonia@email.com",
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
            "cliente_nome": "felipe",
            "cliente_email": "felipe@email.com",
            "tipo_solicitacao": "Análise",
            "valor_patrimonio": 100000
        }
    )

    payload = {
        "event_id": "evt_002",
        "card_id": "card_002",
        "cliente_email": "felipe@email.com",
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
            "cliente_nome": "luiz",
            "cliente_email": "luiz@email.com",
            "tipo_solicitacao": "Análise",
            "valor_patrimonio": 500000
        }
    )

    payload = {
        "event_id": "evt_duplicate",
        "card_id": "card_003",
        "cliente_email": "luiz@email.com",
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