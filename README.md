# Oxalis Coding Assessment

## Ideal Features

Below is an incomplete list of features that I would add to this project if I expected to deliver it to clients for their use.

1. Write additional explanatory documentation, especially installation and usage details.
1. Automatically generate a dummy sales data file so that the user can clone the repository and run the entire container without already having the required `example_sales_data.csv` file.
1. Automatically test all components of the Python code using (e.g.) a `pytest` framework.
1. Add inline comments and complete docstrings to all Python scripts (in a manner similar to my personal toolbox, ["gconanpy"](https://github.com/GregConan/gconanpy)).
1. Modify `oxalis_challenge/data_cleaners.py` to handle multiple transactions per date.
1. Modify `oxalis_challenge/psql_loaders.py` to allow incremental loading.

## Usage

### Requirements

- dbt
- Docker
- Git
- Pip
- Python 3.10+
- Python-Poetry

For a full list of requirements, see `requirements.txt` and `pyproject.toml` in this directory.

### Installation and Usage

1. Install all necessary dependencies.
1. Clone this repository.
1. Run `bash run.sh` from within this top-level directory to build container and models.
1. Open `dbt/oxalis_challenge/target/static_index.html` in your browser to interactively view data models and lineage graph.

## Running the Environment

## Data Model

### Lineage Graph

![Data Models Lineage Graph](lineage_graph_screenshot_2025-05-19.png)

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
