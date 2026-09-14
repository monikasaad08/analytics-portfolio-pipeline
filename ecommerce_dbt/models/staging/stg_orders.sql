{{ config(materialized='view') }}
SELECT
    "order_id",
    "customer_id",
    "order_status",
    "order_purchase_timestamp",
    "order_delivered_customer_date",
    DATEDIFF(day, "order_purchase_timestamp", "order_delivered_customer_date") as days_to_delivery,
    CURRENT_TIMESTAMP() as loaded_at
FROM {{ source('raw', 'OLIST_ORDERS_DATASET') }}
WHERE "order_id" IS NOT NULL