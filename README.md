# Pipeline de Dados Híbrida para Análise da Alfabetização 
> **Pós-Graduação em AI Scientist – FIAP** - Tech Challenge – Fase 2

Pipeline de dados híbrida construída a partir do Databricks, com integração do repositório Github, seguindo a arquitetura Medalhão (Bronze → Silver → Gold).

---
## 1. Contexto do Problema
O Compromisso Nacional Criança Alfabetizada é uma política pública voltada à alfabetização de estudantes dos anos iniciais do ensino fundamental. A iniciativa envolve a participação da União, dos estados, do Distrito Federal e dos municípios e estabelece metas relacionadas ao acompanhamento da alfabetização dos estudantes.  

Em 2023, o Instituto Nacional de Estudos e Pesquisas Educacionais Anísio Teixeira (Inep) realizou a Pesquisa Alfabetiza Brasil, que definiu o ponto de corte de 743 pontos na escala de proficiência do Sistema de Avaliação da Educação Básica (Saeb) para caracterizar o padrão nacional de alfabetização. A partir desse parâmetro, foi desenvolvido o Indicador Criança Alfabetizada, utilizado para apresentar o percentual de estudantes que atingem esse nível de desempenho.

O objetivo desse projeto é criar um fluxo de dados garantindo a integridade, qualidade e consistência da informação.

**Fonte:** [Avaliação da Alfabetização](https://www.gov.br/inep/pt-br/areas-de-atuacao/avaliacao-e-exames-educacionais/avaliacao-da-alfabetizacao).  

## 2. Arquitetura Proposta  

Pipeline de dados híbrida seguindo o padrão da arquitetura de Medalhão para um refinamento progressivo da qualidade dos dados. Segundo [Databricks](https://www.databricks.com/br/blog/what-is-medallion-architecture), a arquitetura medalhão se refere a um design de dados usados para organizar logicamente os dados de um lakehouse, visando melhorar de forma incremental e progressiva a estrutura e a qualidade dos dados à medida que fluem pelas três camadas da arquitetura (Bronze → Prata → Ouro). 

No pipeline proposto neste projeto, há duas especificidades que merecem destaque. A primeira refere-se à origem dos dados da camada Bronze, que ocorre de duas formas distintas: em batch e em streaming. Os dados em batch são estáticos e, em princípio, não possuem alterações programadas em suas fontes. Já os dados em streaming são dinâmicos e atualizados com determinada frequência. Neste projeto, os dados em streaming são gerados artificialmente. A segunda especificidade diz respeito ao tratamento dos dados provenientes do streaming. Nesse caso, é aplicado um filtro responsável por verificar a validade dos registros, classificando-os em duas categorias, dados válidos e dados em quarentena.


| Camada | Função |
|--------|-------|
| **Bronze** | Dados brutos ingeridos das fontes. Não ocorre nenhum tratamento dos dados, apenas o enriquencimento das informações a partir da adição de metadados. |
| **Prata** | Limpeza, tratamento de nulos, padronização de tipos/nomes, validação de consistência e normalização.| 
| **Ouro** |Dados consolidados destinados a projetos finalísticos como análise, contrução de inteligência, visualizações e outros. |

**Dados ingeridos (6):** UF · Meta Alfabetização Brasil · Meta Alfabetização por UF · Meta Alfabetização por Município · Município · Dados de alunos.

## 3. Fluxograma
<img src="images/Fluxo Pipeline Tech2.png" width=2500 height=2600>

## 4. Estrutura do Repositório
```
TechChallenge2/
├── notebooks/         # notebooks Databricks (bronze, streaming, prata, ouro)
├── src/               # scripts para funcionamento do pipeline 
└── images/            # imagens
```

## 5. Forma de Executar  

**Pré-requisitos**
- Projeto GCP com BigQuery habilitado. A chave de integração em formato JSON fica fora do Worspace.  

- Databricks Free Edition com o Volume e a chave de integração enviada para o Volume.  

**Pipeline — ordem de execução dos scripts/notebooks**  

0. `volumes` — criação dos diretórios usados no Databricks usados para armazenamento dos dados e documentos.
1. `ingestao_bronze_batch` — ingestão batch das 7 fontes →  Bronze.
2. `ingestao_bronze_streaming` — gerador de dados simulados e estrutura do streaming → Bronze.
3. `prata` — limpeza, normalização de chaves, decodificação dos dados da camada bronze → Prata.
4. `ouro` — dados completamente tratados e estruturados destinados para os projetos finalísticos → Ouro.
5. `publicar_bigquery` — publicação dos datasets analíticos no Google BigQuery → Ouro.  

## 6. Considerações Finais

Nota-se que ainda há espaço para aprimoramento e consolidação da pipeline de dados proposta. Outro ponto de possível melhora é a estruturação das pastas, visto que os scripts/notebooks responsáveis pelo fluxo dos dados estão dispersos em duas pastas distintas. Trata-se de uma versão preliminar que servirá como base para o TechChallenge3, uma melhor integração entre as bases serão consolidadas nesse repositório.
