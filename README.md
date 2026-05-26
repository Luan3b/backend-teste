Markdown# Mundo Invest — API de Integração e Esteira Pipefy

Este projeto consiste em uma API robusta desenvolvida em **FastAPI** e **Python 3.12** para gerenciar o fluxo de entrada de novos clientes e automatizar o motor de regras de negócios e priorização de cartões na esteira do **Pipefy**, simulando integrações baseadas na API GraphQL v2.

A aplicação adota práticas recomendadas de mercado, como **Arquitetura em Camadas** (Decoupled Layers), **Repository Pattern**, **Inversão de Dependência (SOLID)**, **Idempotência de Webhooks** e **Testes Automatizados Isolados**.

---

## 🛠️ Tecnologias e Frameworks Utilizados

* **FastAPI:** Framework web assíncrono de alta performance.
* **Pydantic v2:** Validação rigorosa de esquemas e tipos de dados.
* **SQLAlchemy ORM:** Mapeamento objeto-relacional para persistência.
* **SQLite:** Banco de dados relacional leve para desenvolvimento local.
* **Pytest:** Framework de testes unitários e de integração.

---

## 🚀 Instruções de Execução Local

### 1. Clonar o Repositório e Acessar o Diretório

```bash
git clone [https://github.com/Luan3b/backend-teste.git](https://github.com/Luan3b/backend-teste.git)
cd backend-teste
```

2. Configurar o Ambiente Virtual (venv) e Instalar Dependências

```Bash
python3 -m venv venv
source venv/bin/activate
pip install -r requisitos.txt
```

3. Executar o Servidor de Desenvolvimento (Uvicorn)
 ```Bash
  uvicorn app.main:app --reload
```

A API inicializará com sucesso e estará acessível em 
```
http://127.0.0.1:8000.
```

🎛️ Painel Integrado de Controle (Substituto do Swagger)
Para testar a aplicação de forma totalmente visual, interativa e simulando cenários de erro (e-mail duplicado, cálculo patrimonial e idempotência), abra o seu navegador e acesse a rota oficial de documentação:
```
👉 http://127.0.0.1:8000/docs
```

🧪 Execução dos Testes Automatizados
Os testes rodam de forma totalmente isolada em um banco de dados SQLite em memória (sqlite:///:memory:), garantindo velocidade e integridade.
Com o ambiente virtual ativo, execute na raiz do projeto:
```Bash
python -m pytest -v
```
Cenários cobertos:
```
test_webhook_prioridade_alta: Valida o gatilho do webhook e classificação patrimonial VIP (>= R$ 200.000,00).
```
```
test_webhook_prioridade_normal: Valida classificação patrimonial padrão (< R$ 200.000,00).
```
```
test_webhook_evento_duplicado: Valida a barreira de segurança de Idempotência (Status 409).
```
📡 Exemplos de Requisição (cURL)
Fluxo 1: Criação de Cliente ```(POST /clientes)```

```Bash
curl -X 'POST' \
  '[http://127.0.0.1:8000/clientes](http://127.0.0.1:8000/clientes)' \
  -H 'Content-Type: application/json' \
  -d '{
    "cliente_nome": "luan borba",
    "cliente_email": "luan@email.com",
    "tipo_solicitacao": "Aporte de Capital",
    "valor_patrimonio": 250000.00
  }'
```
Fluxo 2: Disparo de Webhook do Pipefy ```(POST /webhooks/pipefy/card-updated)```
```Bash
curl -X 'POST' \
  '[http://127.0.0.1:8000/webhooks/pipefy/card-updated](http://127.0.0.1:8000/webhooks/pipefy/card-updated)' \
  -H 'Content-Type: application/json' \
  -d '{
    "event_id": "evt_MI_1001",
    "card_id": "card_pipefy_999",
    "cliente_email": "luan@email.com",
    "timestamp": "2026-05-24T19:30:00Z"
  }'
```
☁️ Visão de Produção (AWS)

Em um ambiente produtivo, a arquitetura poderia evoluir para um modelo serverless e distribuído utilizando serviços gerenciados da AWS, garantindo escalabilidade, resiliência e alta disponibilidade.

🗺️ Arquitetura Proposta

Amazon API Gateway → Exposição segura dos endpoints HTTP.

AWS Lambda → Processamento serverless das regras de negócio.

Amazon RDS / Aurora PostgreSQL → Persistência relacional dos clientes.

Amazon DynamoDB → Controle de idempotência dos webhooks.

Amazon SQS → Desacoplamento e processamento assíncrono de eventos.

Amazon CloudWatch → Logs, métricas e monitoramento de performance.

Amazon Route 53 → Gerenciamento de DNS e failover regional automatizado.


⚙️ Fluxo ArquiteturalPlaintextClient Request
```
      │
      ▼
 API Gateway
      │
      ▼
Lambda / FastAPI
      │
      ▼
RDS PostgreSQL
      │
      ▼
    SQS
      │
      ▼
Webhook Processor
      │
      ▼
  Pipefy API
```
📈 Estratégia de EscalabilidadeA

utilização do AWS Lambda permite escalabilidade automática e horizontal baseada no volume exato de requisições recebidas, reduzindo o custo ocioso a zero.

O desacoplamento via Amazon SQS reduz os impactos de picos repentinos de tráfego (Spike Buffering) e aumenta a resiliência no processamento assíncrono dos webhooks.

O DynamoDB é escalado especificamente para o controle avançado de idempotência, devido à sua latência na casa dos milissegundos e alto desempenho para consultas rápidas por ```event_id```.

O Amazon RDS/Aurora assume a responsabilidade pelos dados relacionais dos clientes, garantindo consistência transacional ACID e integridade absoluta das informações cadastrais.

🧱 Resiliência a Desastres (Failover de Região Global)

Em um cenário de indisponibilidade regional da AWS, o Amazon Route 53 detecta automaticamente falhas de conectividade por meio de Health Checks de borda e redireciona todo o tráfego global para uma região secundária saudável em poucos segundos.

Os registros de eventos processados anteriormente são replicados em tempo real utilizando DynamoDB Global Tables, garantindo a continuidade do mecanismo de idempotência mesmo após o failover entre continentes.

Para o banco relacional, o Amazon Aurora Global Database permite replicação síncrona entre regiões e promoção automatizada da réplica secundária a cluster de escrita principal em menos de um minuto, mitigando a indisponibilidade e minimizando a perda de dados.

Essa estratégia proporciona:

Alta disponibilidade contínua (Active-Active)

Recuperação automatizada contra desastres de infraestrutura

Continuidade operacional estável

Baixíssimo tempo de recuperação (RTO)

Perda de dados próxima a zero (RPO)
