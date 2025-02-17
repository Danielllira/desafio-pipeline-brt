from prefect import task
import requests
import logging
import pandas as pd

import os
from datetime import datetime
import json

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

import subprocess



logger = logging.getLogger(__name__)

@task
def fetch_brt_data() -> dict:
    """
    Captura os dados da API do BRT.
    Retorna: Json
    """
    url = "https://dados.mobilidade.rio/gps/brt"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        logger.info("Dados extraídos com sucesso!")
        return data
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro ao extrair dados: {e}")
        return None
    
@task
def save_raw_data(data: dict) -> dict:
    '''
    Task para salvar os dados brutos (JSON) em um arquivo.
    Retorna: Json
    '''
    if not data:
        logger.error("Nenhum dado recebido para salvar.")
        return None

    # Salva os dados brutos em JSON
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = f"data/raw_data/brt_data_{timestamp}.json"
    os.makedirs("data/raw_data", exist_ok=True)


    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    logger.info(f"Dados brutos salvos em: {file_path}")

    return data

@task
def turn_data_into_dataframe(data: dict) -> pd.DataFrame:
    """
    Task para transformar os dados em um pandas Dataframe
    Retorna: Pandas Dataframe
    """
    if not data:
        logger.error("Nenhum dado recebido para processamento.")
        return None
    
    df = pd.DataFrame(data['veiculos'])
    return df

@task
def transform_datetime_column(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Task para transformar a coluna dataHora em um formato legível e cria colunas separadas para data e hora.
    Retorna: Pandas Dataframe com as colunas transformadas.
    '''
    # Renomeia a coluna 'dataHora' para 'datahora'
    df = df.rename(columns={'dataHora': 'datahora'})
    
    # Converte timestamp de milissegundos para datetime
    df['datahora'] = pd.to_datetime(df['datahora'], unit='ms', origin='unix')

    # Converte para o fuso horário de Brasília (UTC-3)
    df['datahora'] = df['datahora'].dt.tz_localize('UTC').dt.tz_convert('America/Sao_Paulo')
    
    # Cria colunas separadas para data e hora
    df['data'] = df['datahora'].dt.date.astype(str)  # Extrai a data
    df['hora'] = df['datahora'].dt.time.astype(str)  # Extrai a hora
    
    logger.info("Coluna 'datahora' transformada com sucesso!")
    return df

@task
def handle_null_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Task para tratar valores vazios no DataFrame.
    Retorna: DataFrame com valores vazios convertidos para None.
    """
    try:
        # Converte strings vazias e espaços em branco para None
        df = df.replace(' ', None)
        df = df.replace('', None)

        # Converte a coluna 'ignicao' para booleano
        df['ignicao'] = df['ignicao'].astype(bool)
        
        logger.info("Valores vazios tratados com sucesso!")
        return df
        
    except Exception as e:
        logger.error(f"Erro ao tratar valores vazios: {e}")
        return df
    

    
@task
def reorder_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Reorganiza as colunas para seguir um padrão de consistência.
    """
    colunas_ordenadas = [
        "codigo", "placa", "linha", "data", "hora", 
        "latitude", "longitude", "velocidade", "sentido", "trajeto", 
        "direcao", "ignicao", "hodometro", "id_migracao_trajeto", "datahora"
    ]
    
    # Filtra e reorganiza as colunas (garante que todas existam no DataFrame)
    df = df[[col for col in colunas_ordenadas if col in df.columns]]

    logger.info("Colunas reorganizadas com sucesso!")
    return df

@task
def save_processed_data(df: pd.DataFrame) -> str:
    '''
    Task para salvar os dados processados em um arquivo CSV.
    Retorna: Caminho do arquivo salvo (str).
    '''
    if df is None:
        logger.error("Nenhum dado recebido para salvar em CSV.")
        return None

    # Cria diretório se não existir
    os.makedirs("data/processed_data", exist_ok=True)

    # Define nome do arquivo baseado na data e hora da execução
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = f"data/processed_data/brt_data_{timestamp}.csv"

    # Salva o dataframe em CSV
    df.to_csv(file_path, index=False, encoding='utf-8')

    logger.info(f"Dados salvos em {file_path}")
    return file_path

@task
def load_data_into_postgres(file_path: str, db_url: str) -> None:
    """
    Task para carregar os dados do CSV para o PostgreSQL.
    Retorna: None
    """
    if file_path is None:
        logger.error("Nenhum arquivo CSV fornecido para carregar no PostgreSQL.")
        return

    try:
        # Criar conexão com PostgreSQL
        engine = create_engine(db_url)

        # Ler CSV para DataFrame
        df = pd.read_csv(file_path)

        # Inserir dados no banco
        df.to_sql("brt_gps", engine, schema="stage", if_exists="append", index=False, method="multi")

        logger.info("Dados carregados no PostgreSQL com sucesso!")

    except SQLAlchemyError as e:
        logger.error(f"Erro ao carregar dados no PostgreSQL: {e}")

@task
def run_dbt(dbt_project_path: str):
    """
    Executa o comando DBT para rodar os modelos do projeto DBT.
    """
    # Muda para o diretório do DBT
    os.chdir(dbt_project_path)
    
    # Executa o comando dbt run
    result = subprocess.run(["dbt", "run"], capture_output=True, text=True)
    
    # Log de sucesso ou falha
    if result.returncode != 0:
        logger.error(f"DBT run falhou: {result.stderr}")
    else:
        logger.info("DBT run executado com sucesso!")
    
    return result.stdout