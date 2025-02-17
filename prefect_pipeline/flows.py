from prefect import Flow
from prefect_pipeline.tasks import (
    fetch_brt_data, 
    save_raw_data,
    turn_data_into_dataframe, 
    transform_datetime_column, 
    handle_null_values,
    reorder_columns,
    save_processed_data, 
    load_data_into_postgres
)
from prefect_pipeline.schedules import brt_pipeline_schedule

DB_URL = "postgresql://myuser:mypassword@localhost:5432/brt_database"

with Flow("BRT Data Pipeline", schedule=brt_pipeline_schedule) as flow:
    # Captura os dados da API
    raw_data = fetch_brt_data()

    # Salva os dados brutos (JSON)
    raw_data = save_raw_data(raw_data)  # Chama a nova task e atualiza raw_data

    # Transforma em DataFrame
    df = turn_data_into_dataframe(raw_data)
    
    # Ajusta dataHora
    df_transformed = transform_datetime_column(df)

    # Trata valores nulos
    df_cleaned = handle_null_values(df_transformed)
    
    # Reordena as columas
    df_ordered = reorder_columns(df_cleaned) 

    # Salva CSV
    file_path = save_processed_data(df_ordered)
    
    # Carrega no PostgreSQL
    load_data_into_postgres(file_path, db_url=DB_URL)

    