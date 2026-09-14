{{ config(materialized='table') }}
SELECT
    o."order_id",
    o."customer_id",
    c."customer_city",
    o."order_status",
    o."order_purchase_timestamp"::DATE AS order_date,
    COUNT(oi."order_item_id") AS item_count,
    SUM(oi."price") AS total_order_value,
    o.days_to_delivery
FROM {{ ref('stg_orders') }} AS o
LEFT JOIN {{ ref('stg_customers') }} AS c
    ON o."customer_id" = c."customer_id"
LEFT JOIN {{ source('raw', 'OLIST_ORDER_ITEMS_DATASET') }} AS oi
    ON o."order_id" = oi."order_id"
    WHERE o."order_id" IS NOT NULL 
  AND o."customer_id" IS NOT NULL
GROUP BY
    o."order_id",
    o."customer_id",
    c."customer_city",
    o."order_status",
    o."order_purchase_timestamp"::DATE,
    o.days_to_delivery