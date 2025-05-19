#!/usr/bin/env bash

# Run Python script to extract sales data, clean it, and add it to SQL DB
poetry run python app.py data/example_sales_data.csv;

# Move into the dbt directory for dbt setup
cd dbt/oxalis_challenge;

# Setup dbt and build data models
poetry run dbt run;

# Create documentation showing data flow
poetry run dbt docs generate --static --write-json --print;
