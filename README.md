# Pipeline de Dados Híbrida para Análise da Alfabetização no Brasil  
> **Pós-Graduação em AI Scientist – FIAP** - Tech Challenge – Fase 2

Pipeline de dados híbrida (Batch e Streaming) construída a partir do Databricks integrada com o repositório Github, seguindo a arquitetura medalhão (Bronze → Silver → Gold).

---
## 1. Contexto do Problema
O Compromisso Nacional Criança Alfabetizada é uma política pública voltada à alfabetização de estudantes dos anos iniciais do ensino fundamental. A iniciativa envolve a participação da União, dos estados, do Distrito Federal e dos municípios e estabelece metas relacionadas ao acompanhamento da alfabetização dos estudantes.  

Em 2023, o Instituto Nacional de Estudos e Pesquisas Educacionais Anísio Teixeira (Inep) realizou a Pesquisa Alfabetiza Brasil, que definiu o ponto de corte de 743 pontos na escala de proficiência do Sistema de Avaliação da Educação Básica (Saeb) para caracterizar o padrão nacional de alfabetização. A partir desse parâmetro, foi desenvolvido o Indicador Criança Alfabetizada, utilizado para apresentar o percentual de estudantes que atingem esse nível de desempenho.

**Fonte:** [Avaliação da Alfabetização](https://www.gov.br/inep/pt-br/areas-de-atuacao/avaliacao-e-exames-educacionais/avaliacao-da-alfabetizacao).
## 2. Arquitetura Proposta  
| Camada | Função |
|--------|-------|
| **Bronze** | Dados brutos ingeridos das fontes, sem transformação, histórico completo + metadados de ingestão |
| **Prata** | Limpeza, tratamento de nulos, padronização de tipos/nomes, validação de consistência, **normalização de chaves e integração das 6 bases** | 
| **Ouro** | Datasets analíticos: indicador por município, metas × resultados, evolução temporal |

**Dados ingeridos (6):** UF · Meta Alfabetização Brasil · Meta Alfabetização por UF · Meta Alfabetização por Município · Município · Dados de alunos.

**Ingestão híbrida:**
- **Batch** — dados históricos de metas, municípios e agregados nacionais (Base dos Dados).
- **Streaming** — eventos quase-real-time (novas medições do indicador) via produtor
  Python e Structured Streaming.


## 3. Fluxograma
<img src="images/Fluxo Pipeline Tech2.png" width=2500 height=2600>

## 4. Estrutura do Repositório
```
tech-challenge-alfabetizacao/
├── notebooks/         # notebooks Databricks (bronze, streaming, prata, ouro)
├── src/               # scripts para funcionamento do pipeline 
└── images/            # imagens
```

## 5. Forma de Executar
**Pré-requisitos**
- Projeto GCP com BigQuery habilitado. A chave de integração em formato JSON fica fora do Worspace.  

- Databricks Free Edition com o Volume e a chave de integração enviada para o Volume.

**Pipeline — ordem de execução dos scripts/notebooks **  

0. `volumes` — criação dos diretórios usados no Databricks usados para armazenamento dos dados e documentos.
1. `ingestao_bronze_batch` — ingestão batch das 7 fontes →  Bronze.
2. `ingestao_bronze_streaming` — gerador de dados simulados e estrutura do streaming → Bronze.
3. `prata` — limpeza, normalização de chaves, decodificação e intregração → Prata.
4. `ouro` — dados completamente tratados e estruturados usados para os projetos finalísticos → Ouro.
5. `publicar_bigquery` — datasets analíticos → Ouro.  

## 6. Considerações Finais

Nota-se que ainda há espaço para aprimoramento e consolidação da pipeline de dados proposta. Outro ponto de possível melhora é a estruturação das pastas, visto que os scripts/notebooks responsáveis pelo fluxo dos dados estão dispersos em duas pastas distintas. Trata-se de uma versão preliminar que servirá como base para o TechChallenge3, uma melhor integração entre as bases serão consolidadas nesse repositório.
