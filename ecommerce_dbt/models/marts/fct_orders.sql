-- Takes the intermediate table and adds business logic (categorizing orders as high/medium/low value)

{{ config(materialized='table') }}

SELECT
    "order_id",
    "customer_id",
    "customer_city",
    order_date,
    "order_status",
    item_count,
    total_order_value,
    days_to_delivery,
    CASE 
        WHEN total_order_value > 500 THEN 'High Value'
        WHEN total_order_value > 100 THEN 'Medium Value'
        ELSE 'Low Value'
    END as order_value_segment
FROM {{ ref('int_order_summary') }}
WHERE total_order_value > 0