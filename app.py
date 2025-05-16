#!/usr/bin/env python3

"""
Oxalis Challenge
Greg Conan: gregmconan@gmail.com
Created: 2025-05-13
Updated: 2025-05-15
"""
# Import standard libraries
import argparse
# import os
import pdb
# import re
# import sys
from typing import Any  # , Literal

# Import third-party PyPI libraries
import inflection
# import numpy as np
import pandas as pd

# Import remote custom libraries
from gconanpy.cli import Valid
from gconanpy.debug import print_tb_of
from gconanpy.metafunc import DATA_ERRORS, WrapFunction


def main() -> None:
    cli_args = get_cli_args()
    df = pd.read_csv(cli_args["sales_data_file"],
                     na_values=("na", "Error"))
    df = clean_sales_data(df, interpolate=cli_args["interpolate"])
    pdb.set_trace()


class NumbersIn:
    _NumType = int | float

    # Regex patterns: TODO Insert comments into strings (re.X)
    DIGITS = r"(\d+)"  # Match all digits in the string.
    PERCENT = r"(?:[0\.]*)([^%\s]+)(?:\%*)"  # TODO explain

    @staticmethod
    def str_ser(ser: pd.Series, as_type: type[_NumType],
                re_pat: str = DIGITS) -> pd.Series:
        """  _summary_

        :param ser: pd.Series[str], _description_
        :param as_type: type[_NumType], _description_
        :return: pd.Series[_NumType], _description_
        """
        return ser.str.extract(re_pat, expand=False).astype(as_type)

    @classmethod
    def pct_ser(cls, pct_ser: pd.Series) -> pd.Series:
        """  _summary_

        :param pct_ser: pd.Series[str], _description_
        :return: pd.Series[float], _description_
        """
        return cls.str_ser(pct_ser, float, cls.PERCENT) / 100

    @classmethod
    def str_col(cls, df: pd.DataFrame, col_name: str,
                as_type: type[_NumType]) -> pd.DataFrame:
        """ _summary_

        :param df: pd.DataFrame, _description_
        :param col_name: str, _description_
        :param as_type: type[_NumType], _description_
        :return: pd.DataFrame, _description_
        """
        df[col_name] = cls.str_ser(df[col_name], as_type)
        return df


def clean_sales_data(df: pd.DataFrame, interpolate: bool = False
                     ) -> pd.DataFrame:
    # Standardize column names: lowercase and underscore-separated
    underscorize = WrapFunction(inflection.parameterize, separator="_")
    # TODO Remove dependence on gconanpy?
    df.rename(columns=underscorize, inplace=True)

    # Standardize date format
    df["date"] = pd.to_datetime(df["date"], format="mixed")

    # Standardize store ID numbers
    df = NumbersIn.str_col(df, "store_id", int)

    try:
        # Standardize transaction ID numbers
        # TODO: Should I keep the "TRX" string preceding txn ID nums?
        if interpolate:
            txn_IDs = NumbersIn.str_ser(df["transaction_id"], float)
            df["transaction_id"] = txn_IDs.interpolate("linear").astype(int)
        else:
            df.dropna(inplace=True)

        df["region"] = df["region"].str.title().str.strip()  # TODO inplace
        df["discount"] = NumbersIn.pct_ser(df["discount"])

        return df
    except DATA_ERRORS as err:
        print_tb_of(err)
        pdb.set_trace()
        print(err)
        raise err


def get_cli_args() -> dict[str, Any]:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "sales_data_file",
        type=Valid.readable_file
    )
    parser.add_argument(
        "--interpolate",
        action="store_true",
        help=("Include this argument to fill missing data by interpolating "
              "from the values before and after each missing data value. "
              "By default, missing data will simply be dropped instead.")
    )
    return vars(parser.parse_args())


if __name__ == "__main__":
    main()
