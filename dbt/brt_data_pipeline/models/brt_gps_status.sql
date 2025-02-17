{{ config(materialized='table') }}
SELECT 
    codigo AS id_onibus,
    latitude,   
    longitude,
    velocidade    
FROM {{ ref('brt_gps') }}