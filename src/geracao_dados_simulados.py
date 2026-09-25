########################################################
# LIBS
########################################################
import pandas as pd
import numpy as np
import json
import os
import time
from datetime import datetime, timezone
import random
import uuid


########################################################
# DEFINIÇÃO DE OBJETOS
########################################################

##### OS 20 MUNICÍPIOS MAIS POPULOSOS DO BRASIL
##### CÓDIGO DO IBGE E UF
##### OS DADOS SIMULADOS SERÃO REFERENTES À TABELA "Município"
##### EM CAMADAS POSTERIORES OS DADOS SERÃO AGREGADOS
MUNICIPIO = [
    (3550308, "SP"),  # São Paulo
    (3304557, "RJ"),  # Rio de Janeiro
    (5300108, "DF"),  # Brasília
    (2304400, "CE"),  # Fortaleza
    (2927408, "BA"),  # Salvador
    (3106200, "MG"),  # Belo Horizonte
    (1302603, "AM"),  # Manaus
    (4106902, "PR"),  # Curitiba
    (2611606, "PE"),  # Recife
    (5208707, "GO"),  # Goiânia
    (1501402, "PA"),  # Belém
    (4314902, "RS"),  # Porto Alegre
    (3518800, "SP"),  # Guarulhos
    (3509502, "SP"),  # Campinas
    (2111300, "MA"),  # São Luís
    (2704302, "AL"),  # Maceió
    (5002704, "MS"),  # Campo Grande
    (3304904, "RJ"),  # São Gonçalo
    (2211001, "PI"),  # Teresina
    (2507507, "PB")  # João Pessoa
    ]

#### TIPO DE REDE DE ENSINO
#### 2 - Estadual, 3 - Municipal, 4 - Privada
REDE = [2, 3, 4]

########################################################
# GERAÇÃO DOS EVENTOS
########################################################

#### SIMULANDO DADOS DOS MUNICÍPIOS NO ANO DE 2025
def simulador():
    codigo_municipio, uf = random.choice(MUNICIPIO)
    return {
        "id": str(uuid.uuid4()),  #Generate a random UUID in a cryptographically-secure method according to (RFC 9562, §5.4).
        "ano": 2025, 
        "id_municipio": int(codigo_municipio),
        "sigla_uf": uf,
        "rede": int(np.random.choice(REDE)),
        "serie": 2, 
        "taxa_alfabetizacao": round(np.random.normal(loc = 65, scale = 20), 1),
        "media_portugues": round(np.random.normal(loc = 650, scale = 220), 1),
        "_momento_ingestao": datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S"),
        "_data_ingestao": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "_origem": "simulado"}


########################################################
# ESCRITA DOS EVENTOS
########################################################

### ARMAZENA OS EVENTOS NO DIRETÓRIO
def armazenar(eventos: list[dict], diretorio: str) -> str:
    
    #
    os.makedirs(diretorio, exist_ok=True)
    marcador_tempo = datetime.now().strftime('%Y%m%d_%H%M%S')

    #
    nome_arquivo = f"eventos_{marcador_tempo}.json"
    caminho_arquivo  = os.path.join(diretorio, nome_arquivo)

    #
    with open(caminho_arquivo , "w", encoding="utf-8") as file:
        for i in eventos:
            file.write(json.dumps(i, ensure_ascii=False) + "\n")
            
    return caminho_arquivo 

########################################################
# PRODUÇÃO DOS EVENTOS SIMULADOS
########################################################

### PRODUTOR
def produtor(diretorio: str, num_lotes: int = 10, num_eventos: int = 20, tempo: float = 3.0):
    
    #
    ARQUIVOS = []
    for i in range(num_lotes):
        lote = [simulador() for _ in range(num_eventos)]
        dir = armazenar(lote, diretorio)
        ARQUIVOS.append(dir)
        print(f"Geração de {len(lote)} novos eventos no lote {i + 1}|{num_lotes} no diretório {dir}")

        #
        if i < num_lotes - 1:
            time.sleep(tempo)
    return ARQUIVOS