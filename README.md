# Oxalis Coding Assessment

## Introduction



## Running the Environment

### 1. Build Container and Models

```bash
bash run.sh
```

### 2. Verify Outputs

- Check the transformed data in PostgreSQL.

## Data Model

TODO

## Directory Structure

```sh
.
├── Dockerfile
├── README.md
├── app.py
├── data/
│   └── example_sales_data.csv
├── dbt/
│   └── oxalis_challenge/
│       ├── README.md
│       ├── analyses
│       ├── dbt_packages
│       ├── dbt_project.yml
│       ├── macros
│       ├── models
│       │   ├── intermediate
│       │   │   ├── int_ledger__transactions.sql
│       │   │   └── properties.yml
│       │   ├── marts
│       │   │   ├── dim_ledger__product.sql
│       │   │   ├── dim_ledger__store.sql
│       │   │   ├── fct_ledger__transactions.sql
│       │   │   └── properties.yml
│       │   ├── report
│       │   │   ├── rpt_ledger__revenue.sql
│       │   │   └── rpt_ledger__sales_qty.sql
│       │   ├── sources.yml
│       │   └── staging
│       │       ├── properties.yml
│       │       └── stg_ledger__transactions.sql
│       ├── profiles.yml
│       │   ├── run_results.json
│       │   └── semantic_manifest.json
│       └── tests
├── docker-compose.yml
├── oxalis_challenge
│   ├── __init__.py
│   ├── cli.py
│   ├── config.py
│   ├── data_cleaners.py
│   └── psql_loaders.py
├── poetry.lock
├── pyproject.toml
├── requirements.txt
└── run.sh
```