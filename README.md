Markdown# Mundo Invest — API de Integração e Esteira Pipefy

Este projeto consiste em uma API robusta desenvolvida em **FastAPI** e **Python 3.12** para gerenciar o fluxo de ingresso de novos clientes e automatizar o motor de regras de negócios e priorização de cards na esteira do **Pipefy**, simulando integrações baseadas na API GraphQL v2.

A aplicação adota práticas recomendadas de mercado, como **Arquitetura em Camadas** (Decoupled Layers), **Repository Pattern**, **Inversão de Dependência (SOLID)**, **Idempotência de Webhooks** e **Testes Automatizados Isolados**.

---

## 🛠️ Tecnologias e Frameworks Utilizados

* **FastAPI:** Framework web assíncrono de alta performance.
* **Pydantic v2:** Validação rigorosa de esquemas e tipos de dados.
* **SQLAlchemy ORM:** Mapeamento objeto-relational para persistência.
* **SQLite:** Banco de dados relacional leve para desenvolvimento local.
* **Pytest:** Framework de testes unitários e de integração.

---

## 🚀 Instruções de Execução Local

### 1. Clonar o Repositório e Acessar o Diretório
```bash
git clone <url-do-seu-repositorio>
cd backend-teste
2. Configurar o Ambiente Virtual (venv) e Instalar DependênciasBashpython3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
3. Executar o Servidor de Desenvolvimento (Uvicorn)Bashuvicorn app.main:app --reload
A API inicializará com sucesso e estará acessível em http://127.0.0.1:8000.🎛️ Painel Integrado de Controle (Substituto do Swagger)Para testar a aplicação de forma totalmente visual, interativa e simulando cenários de erro (e-mail duplicado, cálculo patrimonial e idempotência), abra o seu navegador e acesse a rota oficial de documentação:👉 http://127.0.0.1:8000/docs🧪 Execução dos Testes AutomatizadosOs testes rodam de forma totalmente isolada em um banco de dados SQLite em memória (sqlite:///:memory:), garantindo velocidade e integridade.Com o ambiente virtual ativo, execute na raiz do projeto:Bashpython -m pytest -v
Cenários cobertos:test_webhook_prioridade_alta: Valida o gatilho do webhook e classificação patrimonial VIP ($\ge R\$$ 200.000,00).test_webhook_prioridade_normal: Valida classificação patrimonial padrão ($< R\$$ 200.000,00).test_webhook_evento_duplicado: Valida a barreira de segurança de Idempotência (Status 409).📡 Exemplos de Requisição (cURL)Fluxo 1: Criação de Cliente (POST /clientes)Bashcurl -X 'POST' \
  '[http://127.0.0.1:8000/clientes](http://127.0.0.1:8000/clientes)' \
  -H 'Content-Type: application/json' \
  -d '{
    "cliente_nome": "João Silva",
    "cliente_email": "joao@email.com",
    "tipo_solicitacao": "Aporte de Capital",
    "valor_patrimonio": 250000.00
  }'
Fluxo 2: Disparo de Webhook do Pipefy (POST /webhooks/pipefy/card-updated)Bashcurl -X 'POST' \
  '[http://127.0.0.1:8000/webhooks/pipefy/card-updated](http://127.0.0.1:8000/webhooks/pipefy/card-updated)' \
  -H 'Content-Type: application/json' \
  -d '{
    "event_id": "evt_MI_1001",
    "card_id": "card_pipefy_999",
    "cliente_email": "joao@email.com",
    "timestamp": "2026-05-24T19:30:00Z"
  }'


# 🚀 Visão de Produção (AWS)

Em um ambiente produtivo, a arquitetura poderia evoluir para um modelo serverless e distribuído utilizando serviços gerenciados da AWS, garantindo escalabilidade, resiliência e alta disponibilidade.

## Arquitetura Proposta

* **Amazon API Gateway** → exposição segura dos endpoints HTTP
* **AWS Lambda** → processamento serverless das regras de negócio
* **Amazon RDS / Aurora PostgreSQL** → persistência relacional dos clientes
* **Amazon DynamoDB** → controle de idempotência dos webhooks
* **Amazon SQS** → desacoplamento e processamento assíncrono de eventos
* **Amazon CloudWatch** → logs, métricas e monitoramento
* **Amazon Route 53** → gerenciamento de DNS e failover regional

---

## Fluxo Arquitetural

```text
Client Request
↓
API Gateway
↓
Lambda / FastAPI
↓
RDS PostgreSQL
↓
SQS
↓
Webhook Processor
↓
Pipefy API
```

---

## Estratégia de Escalabilidade

A utilização de AWS Lambda permitiria escalabilidade automática baseada no volume de requisições recebidas.

O desacoplamento via Amazon SQS reduziria impactos de picos de tráfego e aumentaria a resiliência no processamento dos webhooks.

O DynamoDB seria utilizado no controle de idempotência devido à sua baixa latência e alta performance para consultas rápidas por `event_id`.

Já o Amazon RDS/Aurora seria responsável pelos dados relacionais dos clientes, garantindo consistência transacional e integridade das informações cadastrais.

---

# 🚀 Resiliência a Desastres (Region Failover)

Em um cenário de indisponibilidade regional da AWS, o Amazon Route 53 poderia detectar automaticamente falhas de conectividade através de Health Checks e redirecionar o tráfego para uma região secundária saudável.

Os registros de eventos processados previamente poderiam ser replicados utilizando DynamoDB Global Tables, garantindo continuidade do mecanismo de idempotência mesmo após o failover.

Para o banco relacional, o Amazon Aurora Global Database permitiria replicação entre regiões e promoção automática da réplica secundária em caso de desastre, reduzindo indisponibilidade e minimizando perda de dados.

Essa estratégia proporcionaria:

* Alta disponibilidade
* Recuperação automática
* Continuidade operacional
* Baixo tempo de recuperação (RTO)
* Mínima perda de dados (RPO)

---
