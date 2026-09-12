# Growth Pro - Pipeline de BI e Automacao (exemplo de arquitetura)

Demonstracao de um pipeline de Business Intelligence modular: conexao a APIs, agregacao de dados, dashboards, calculo de KPIs, relatorios e automacoes.

## O que este projeto demonstra

Uma arquitetura de pipeline organizada em modulos independentes:

- api_connector.py - conectores para fontes de dados (ex: Shopify, Google Sheets)
- data_aggregator.py - agregacao de dados e calculo de KPIs (receita total, ticket medio)
- dashboards.py - geracao de dashboards de vendas, performance e analise
- reports.py - geracao de relatorios em HTML e Excel
- automations.py - integracao com n8n, Slack e agendamento de automacoes
- main.py - orquestra o pipeline completo em 6 etapas

## Importante

Este e um projeto de demonstracao de arquitetura, nao uma integracao em producao. O pipeline roda com dados sinteticos de exemplo (gerados na etapa 2 do main.py). O conector para Shopify esta implementado, mas a chamada real esta comentada no codigo - nao ha integracao ativa com API externa nesta versao.

## Stack

Python, Pandas.

## Como rodar

pip install -r requirements.txt
python src/main.py

