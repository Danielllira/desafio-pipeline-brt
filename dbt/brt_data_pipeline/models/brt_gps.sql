{{ config(materialized='table') }}
SELECT DISTINCT ON (codigo, datahora) *
FROM {{ source('brt_gps', 'brt_gps') }}
ORDER BY codigo, datahora, id