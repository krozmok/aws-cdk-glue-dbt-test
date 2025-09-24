{{ 
    config(
        materialized='incremental',
        incremental_strategy='insert_overwrite',
        partition_by = ['year'],
        file_format='parquet'
    ) 
}}

SELECT *
FROM {{ source('vigia_dl_db_raw', '`modelo-financiero_ca_cruce`') }}
WHERE year = '2017'