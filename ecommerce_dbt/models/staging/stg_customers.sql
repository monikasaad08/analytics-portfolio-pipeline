{{ config(materialized='view') }}
SELECT
    "customer_id",
    "customer_unique_id",
    "customer_city",
    "customer_state",
    CURRENT_TIMESTAMP() as loaded_at
FROM {{ source('raw', 'OLIST_CUSTOMERS_DATASET') }}
WHERE "customer_id" IS NOT NULL