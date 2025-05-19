#!/usr/bin/env python3

"""
Oxalis Challenge: Classes to load Pandas DataFrames into PostgreSQL DB tables
Greg Conan: gregmconan@gmail.com
Created: 2025-05-18
Updated: 2025-05-18
"""
# Import third-party PyPI libraries
import pandas as pd
# import pdb  # Uncomment for interactive manual debugging
import sqlalchemy as sa


class PostgresTableLoader:
    CHUNK_SIZE = 10000

    # Instance variables
    df: pd.DataFrame  # Sales data df
    name: str  # PostgreSQL table name
    schema: str  # PostgreSQL DB schema name

    # Save all query results in instance variable to review when debugging/etc
    responses: list[sa.engine.CursorResult | int]  # int from pd.to_sql

    def __init__(self, df: pd.DataFrame, table_name: str, db_URI: str,
                 schema: str = "public") -> None:
        self.df = df
        self.name = table_name
        self.schema = schema

        self.eng = sa.create_engine(db_URI, pool_pre_ping=True)
        self.responses = list()

    def drop_table(self) -> None:
        self.run(f"DROP TABLE {self.schema}.{self.name} CASCADE")

    def has_table(self) -> bool:
        return sa.inspect(self.eng).has_table(self.name)

    def load(self, drop_if_exists: bool = True) -> None:
        if drop_if_exists and self.has_table():
            self.drop_table()
        self.to_sql()

    # TODO Convert to decorator that defines & passes in context manager?
    def run(self, sql_cmd: str) -> None:
        with self.eng.begin() as con:
            self.responses.append(con.execute(sa.text(sql_cmd)))

    def to_sql(self) -> None:
        with self.eng.begin() as con:
            resp = self.df.to_sql(
                name=self.name, con=con, chunksize=self.CHUNK_SIZE,
                schema="public", if_exists="replace", index=False)
            if resp is not None:
                self.responses.append(resp)
