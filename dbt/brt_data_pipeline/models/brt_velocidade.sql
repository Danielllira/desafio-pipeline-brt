{{ config(materialized='table') }}
SELECT
 codigo,
 latitude,
 longitude,
 velocidade
FROM {{ source('stage', 'brt_gps') }}