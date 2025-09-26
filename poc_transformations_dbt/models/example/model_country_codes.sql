{{ 
    config(
        materialized='incremental',
        incremental_strategy='insert_overwrite',
        partition_by = ['country_code'],
        file_format='parquet'
    ) 
}}

SELECT *, current_timestamp as load_dts
FROM {{ source('source_raw', 'country_codes') }}