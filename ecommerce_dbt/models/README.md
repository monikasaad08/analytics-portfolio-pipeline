# dbt Models Documentation

## Staging Layer (`staging/`)

### stg_customers
- **Purpose:** Clean and standardize customer data
- **Source:** `OLIST_CUSTOMERS_DATASET` (raw)
- **Key columns:** customer_id, customer_city, customer_state
- **Tests:** Unique customer_id, not null checks

### stg_orders
- **Purpose:** Clean and standardize order data
- **Source:** `OLIST_ORDERS_DATASET` (raw)
- **Key columns:** order_id, order_status, order_date
- **Calculated:** days_to_delivery

## Intermediate Layer (`intermediate/`)

### int_order_summary
- **Purpose:** Join orders with customers and items, calculate totals
- **Source:** stg_orders + stg_customers + raw order items
- **Key columns:** order_id, customer_id, total_order_value, item_count
- **Aggregation:** SUM of item prices, COUNT of items per order

## Marts Layer (`marts/`)

### fct_orders
- **Purpose:** Final fact table for analytics and Power BI
- **Source:** int_order_summary
- **Key columns:** order_id, customer_id, total_order_value, order_date
- **Business logic:** order_value_segment (High/Medium/Low)
- **Tests:** Unique order_id, not null checks, valid segments

## How to Run

```bash
cd ecommerce_dbt
dbt run      # Run all models
dbt test     # Run all tests
dbt docs generate  # Generate HTML documentation
```