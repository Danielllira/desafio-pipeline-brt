{{ config(materialized='table', schema='stage') }}

SELECT
    codigo 
    latitude
    longitude
    velocidade  
FROM {{ ref('brt_gps') }}  