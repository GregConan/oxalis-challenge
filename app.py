#!/usr/bin/env python3
"""
Oxalis Challenge: Main script to run sales data cleansing and loading
Greg Conan: gregmconan@gmail.com
Created: 2025-05-13
Updated: 2025-05-18
"""
# Import third-party PyPI libraries
import pandas as pd

# Import local custom libraries
from oxalis_challenge.cli import get_cli_args
from oxalis_challenge.config import SQLALCHEMY_DATABASE_URI
from oxalis_challenge.data_cleaners import SalesData
from oxalis_challenge.psql_loaders import PostgresTableLoader


def main() -> None:
    pd.set_option("display.max_columns", None)
    cli_args = get_cli_args()
    sales_data = SalesData.from_data_file_at(cli_args["sales_data_file"])
    loader = PostgresTableLoader(sales_data.df, "raw_transaction",
                                 SQLALCHEMY_DATABASE_URI)
    loader.load()


if __name__ == "__main__":
    main()
