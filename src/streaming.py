########################################################
####LIBS
########################################################
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql import types as T
from pyspark.sql.functions import col
import pyspark
import pandas as pd
import json


########################################################
####SCHEMA
########################################################

#SEM UM SCHEMA DEFINIDO DOS DADOS SIMULADOS OBSERVOU-SE UM ERRO
def schema():
    DDL = """
    id STRING,
    ano INTEGER,
    id_municipio STRING,
    sigla_uf STRING,
    rede INT,
    serie INT,
    taxa_alfabetizacao DOUBLE,
    media_portugues DOUBLE,
    _momento_ingestao STRING,
    _data_ingestao STRING,
    _origem STRING
    """
    return T.StructType.fromDDL(DDL)

########################################################
####STREAM
########################################################
def stream_bronze(
    spark: SparkSession, 
    evento: str, 
    checkpoint_valido: str,
    checkpoint_quarentena: str, 
    destino_valido: str,
    destino_quarentena: str):

    #1. Leitura dos eventos em formato .json (Streaming)
    entrada = (
        spark.readStream
        .schema(schema())
        .json(evento))
    
    #2. Definição da regra para ir para QUARENTENA
    condicao_quarentena = (
    (col("taxa_alfabetizacao") > 100) | 
    (col("taxa_alfabetizacao") < 0) | 
    (col("media_portugues") > 1000) | 
    (col("media_portugues") < 0))

    #3. Filtrar os DataFrames de entrada
    df_valido = entrada.filter(~(condicao_quarentena))
    df_quarentena = entrada.filter(condicao_quarentena)

   #4. Configurar e Iniciar a Stream de Dados VÁLIDOS
    stream_valido = (
        df_valido.writeStream
        .format("delta")
        .outputMode("append")
        .option("checkpointLocation", checkpoint_valido)
        .partitionBy("sigla_uf")
        .trigger(availableNow=True)
        .start(destino_valido)
    )

    #5. Configurar e Iniciar a Stream de QUARENTENA
    stream_quarentena = (
        df_quarentena.writeStream
        .format("delta")
        .outputMode("append")
        .option("checkpointLocation", checkpoint_quarentena)
        .partitionBy("sigla_uf")
        .trigger(availableNow=True)
        .start(destino_quarentena)
    )


    # Retorna ambas as queries para monitoramento externo se necessário
    return stream_valido, stream_quarentena