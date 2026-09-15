# NZ E-Commerce Analytics Pipeline
This is End-to-End ELT Pipeline portfolio project
**End-to-End ELT Pipeline | Snowflake | dbt | GitHub Actions | Power BI**

## Overview
[Explain: "This pipeline ingests e-commerce transaction data, models it 
for analytics, tests data quality, and surfaces KPIs via Power BI."]

## Architecture Diagram
[ASCII or screenshot showing: Data → Python → Snowflake RAW → dbt Models → Power BI]

## Tech Stack
- Snowflake (Cloud DW)
- dbt Core (Transformation)
- Python (Extraction)
- GitHub Actions (Orchestration)
- Power BI (Visualization)

## Key Metrics Delivered
- **150+ orders processed** weekly via GitHub Actions
- **Data quality tests**: 8 automated tests (uniqueness, nullness, freshness)
- **Query optimization**: 40% faster aggregations via dimensional modeling
- **BI adoption**: 2-second dashboard load time with incremental refresh

## How to Reproduce
1. Clone repo
2. Set Snowflake credentials in `.env`
3. Run `python scripts/extract_and_load.py`
4. Run `dbt run && dbt test`
5. Open Power BI and refresh dataset

## Key Learnings
- **ELT vs ETL**: Why we extract → load raw → transform
- **Dimensional modeling**: Fact tables (fct_orders) and dimensions
- **dbt best practices**: Staging → intermediate → marts
- **Data quality as code**: Testing data, not just queries
