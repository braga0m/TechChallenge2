########################################################
#### LIBS
########################################################
import os
import sys
from google.cloud import bigquery
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
import pandas as pd
from google.oauth2 import service_account

########################################################
#### PUBLICAÇÃO - VERSÃO INICIAL
########################################################
# 1. Configurações de destino no GCP
BILLING_ID = 'avaliacao-alfabetizacao-inep'
DATASET_GOLD = "ouro_analytics"
TABELA = 'municipio_unido'
CHAVE_PATH = "/Volumes/workspace/default/inep_avaliacao_alfabetizacao/avaliacao-alfabetizacao-inep-key.json"

destino = f"{BILLING_ID}.{DATASET_GOLD}.{TABELA}"

# 2. Configura a autenticação com a Service Account
CREDENTIALS = service_account.Credentials.from_service_account_file(CHAVE_PATH)

# 3. Inicializa o cliente oficial do BigQuery com as credenciais
client = bigquery.Client(credentials=CREDENTIALS, project=BILLING_ID)

# 4. GARANTE QUE O DATASET EXISTE (Cria se não existir)
dataset_ref = bigquery.Dataset(f"{BILLING_ID}.{DATASET_GOLD}")
dataset_ref.location = "SOUTHAMERICA-EAST1"  # Ou a região onde deseja armazenar (ex: "US")
dataset = client.create_dataset(dataset_ref, exists_ok=True)
print(f"Dataset {DATASET_GOLD} verificado/criado com sucesso.")

# 5. Leitura da camada Gold (Spark)
df_gold = spark.read.format("parquet").load("/Volumes/workspace/default/inep_avaliacao_alfabetizacao/gold/municipio_unido/")

# 6. Converte o DataFrame para Pandas e envia ao BigQuery
job = client.load_table_from_dataframe(
    df_gold.toPandas(),
    destino,
    job_config=bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")
)

job.result()  # Aguarda a conclusão do envio
print(f"Tabela {destino} publicada com sucesso no BigQuery!")
