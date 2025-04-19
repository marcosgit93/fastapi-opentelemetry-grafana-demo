# POC de Observabilidade com FastAPI e OpenTelemetry

Esta é uma Prova de Conceito (POC) demonstrando a implementação de observabilidade em uma aplicação FastAPI utilizando OpenTelemetry e Grafana.

## Stack Tecnológica

- FastAPI (Backend)
- OpenTelemetry (Coleta de logs, métricas e traces)
- Grafana (Visualização)
- Loki (Armazenamento de logs)
- Promtail (Coleta de logs)
- Docker e Docker Compose (Orquestração)

## Requisitos

- Docker
- Docker Compose

## Como Executar

1. Clone o repositório
2. Execute o comando:
```bash
docker-compose up --build
```

## Acessos

- FastAPI: http://localhost:8000
- Grafana: http://localhost:3000
  - Usuário padrão: admin
  - Senha padrão: admin

## Endpoints da API

- `GET /`: Endpoint raiz
- `GET /health`: Verificação de saúde
- `GET /error`: Gera um erro intencional para demonstração

## Dashboard de Logs

O projeto inclui um dashboard pré-configurado no Grafana para visualização dos logs. O dashboard contém:

1. Painel de Logs de Erro
   - Filtra logs que contêm a palavra "error"
   - Atualiza automaticamente a cada 5 segundos
   - Mostra os últimos 15 minutos de logs

2. Painel de Logs da Aplicação
   - Mostra todos os logs da aplicação FastAPI
   - Atualiza automaticamente a cada 5 segundos
   - Mostra os últimos 15 minutos de logs

Para testar a geração de logs:
1. Acesse o endpoint de erro: http://localhost:8000/error
2. Os logs aparecerão automaticamente no dashboard do Grafana

## Configuração da Observabilidade

A aplicação está configurada para coletar:
- Logs (via Promtail e Loki)
- Traces (via OpenTelemetry)
- Métricas (via OpenTelemetry)

### Estrutura de Logs

Os logs são coletados pelo Promtail e enviados para o Loki com os seguintes labels:
- `job`: "fastapi-app" (identifica os logs da aplicação)
- `container`: nome do container Docker
- `stream`: stream de logs do container

### Verificação de Logs

Para verificar se os logs estão sendo coletados corretamente:

```bash
# Logs do Promtail
docker-compose logs promtail

# Logs da aplicação FastAPI
docker-compose logs app

# Logs do Loki
docker-compose logs loki
```

## Solução de Problemas

Se os logs não estiverem aparecendo no Grafana:
1. Verifique se todos os containers estão rodando:
   ```bash
   docker-compose ps
   ```
2. Verifique os logs dos containers para identificar possíveis erros
3. Certifique-se de que a aplicação está gerando logs (acesse os endpoints)
4. Verifique se o Promtail está coletando os logs corretamente
5. Verifique se o Loki está recebendo os logs do Promtail 