#!/usr/bin/env python3

"""
Oxalis Challenge: Sales data cleaner classes
Greg Conan: gregmconan@gmail.com
Created: 2025-05-17
Updated: 2025-05-17
"""
# Import standard libraries
from collections.abc import Callable  # , Iterable
from typing import Any  # , Literal

# Import third-party PyPI libraries
import inflection
# import numpy as np
import pandas as pd


class NumbersIn:
    """ Regex parser to extract numbers for pd.Series[str] """
    NumType = int | float
    df: pd.DataFrame

    # Regex patterns: TODO Insert comments into strings (re.X)
    DIGITS = r"(\d+)"  # Match all digits in the string.
    PERCENT = r"(?:[0\.]*)([^%\s]+)(?:\%*)"  # TODO explain

    @staticmethod
    def str_ser(ser: pd.Series, as_type: type[NumType],
                re_pat: str = DIGITS) -> pd.Series:
        """  _summary_

        :param ser: pd.Series[str], _description_
        :param as_type: type[_NumType], _description_
        :return: pd.Series[_NumType], _description_
        """
        # TODO Verify that this grabs ALL digits before converting to int
        #      in the case of store IDs?
        return ser.str.extract(re_pat, expand=False).astype(as_type)

    @classmethod
    def pct_ser(cls, pct_ser: pd.Series) -> pd.Series:
        """  _summary_

        :param pct_ser: pd.Series[str], _description_
        :return: pd.Series[float], _description_
        """
        return cls.str_ser(pct_ser, float, cls.PERCENT) / 100


class SalesData:
    df: pd.DataFrame

    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df
        self.df.rename(columns=self.underscorize, inplace=True)

        # Standardize store ID numbers
        self.str2num_for_col("store_id", int)
        # self.df = NumbersIn.str_col(self.df, "store_id", int)

        # Alias column names to only define strings once
        DISCOUNT = "discount"
        PAY = "payment_method"
        QTY = "quantity"
        REGION = "region"
        ID_COLS = ("store_id", "transaction_id")
        STORE, TXN = ID_COLS

        self.clean_dates("date")
        self.apply_to_col(DISCOUNT, NumbersIn.pct_ser)

        self.str2num_for_col(TXN, float)

        # Interpolate AFTER grouping by store
        # TODO after validating that within-store it's monotonic increase?
        for _, store_df in self.df.groupby(STORE):

            # Standardize and interpolate transaction IDs
            txn_IDs = store_df[TXN].interpolate("linear")
            self.update_part_of_col(store_df, TXN, txn_IDs)

            # Standardize and interpolate store region
            store_region = store_df[REGION].mode().str.strip().values[0]
            self.update_part_of_col(store_df, REGION, store_region)

        # Normalize payment method and price
        self.df[PAY] = \
            self.df[PAY].str.removesuffix(" Card").fillna("Unknown")
        self.interpolate_price()

        # TODO EXPLICITLY DOCUMENT ASSUMPTION THAT NaN => QTY=1, DISCOUNT=0
        self.df.fillna({QTY: 1, DISCOUNT: 0.0}, inplace=True)

        for col_name in ID_COLS:
            self.change_col_dtype(col_name, int)

        # CUSTOMER_TYPES = {"Regular", "Premium", "Premier"}
        CUSTOMER_TYPES = pd.Series(("Regular", "Premium", "Premier"))
        self.normalize_str_col("customer_type", CUSTOMER_TYPES)

    def apply_to_col(self, col_name: str, convert:
                     Callable[[pd.Series], pd.Series],
                     *args, **kwargs) -> None:
        self.df[col_name] = convert(self.df[col_name], *args, **kwargs)

    def change_col_dtype(self, col_name: str, new_type: type) -> None:
        self.df[col_name] = self.df[col_name].astype(new_type)

    def clean_dates(self, dt_col: str) -> None:
        """ Standardize date format 

        :param dt_ser: pd.Series[str], _description_
        :return: pd.Series[dt.datetime], _description_
        """
        # Alias temporary column names to only define strings once
        TEMP_COLS = ["month_1st", "day_1st", "is_dayfirst"]
        MONTH, DAY, USE_DAY = TEMP_COLS

        col_is_sorted = False

        col_pair = {MONTH: False, DAY: True}
        for new_col, dayfirst in col_pair.items():
            self.df[new_col] = pd.to_datetime(self.df[dt_col], format="mixed",
                                              dayfirst=dayfirst)

            col_is_sorted = (self.df[new_col].is_monotonic_increasing or
                             self.df[new_col].is_monotonic_decreasing)
            if col_is_sorted:
                self.df[dt_col] = self.df[new_col]
                break  # TODO ?

        # If some dates are out of place, then we probably misread day-first
        # dates as month-first dates, so fix those
        if not col_is_sorted:
            diffs = self.df[[MONTH, DAY]].diff().abs()
            self.df[USE_DAY] = diffs[DAY] < diffs[MONTH]
            self.df.loc[self.df[USE_DAY], dt_col] = self.df[DAY]
            self.df.loc[~self.df[USE_DAY], dt_col] = self.df[MONTH]

        self.apply_to_col(dt_col, pd.to_datetime)
        self.df.drop(columns=TEMP_COLS, errors="ignore", inplace=True)

    @staticmethod
    def coerce_str(aberration: str, options: pd.Series) -> str:
        aberration = aberration.strip()
        is_nearest = options.str.contains(aberration)
        if not is_nearest.any():
            is_nearest = options.apply(aberration.__contains__)
        nearest_match = options.loc[is_nearest]
        if nearest_match.size == 1:
            return nearest_match[0]
        else:
            raise ValueError(f"Failed to match {aberration} to one of "
                             f"these options: {options.values}")

    @classmethod
    def from_data_file_at(cls, data_file_path: str) -> "SalesData":
        return cls(pd.read_csv(data_file_path, na_values=("na", "Error"),
                               skipinitialspace=True))

    def interpolate_price(self):
        """ Convert price to number and interpolate 

        :raises ValueError: _description_
        """
        PRICE = "price"
        PRODUCT = "product_name"

        # Standardize prices and convert them to float
        self.df[PRICE] = self.df[PRICE].str.strip().str.removeprefix("$") \
            .astype(float)

        # Fill any missing prices with prices of the same product elsewhere
        for _, product_df in self.df.groupby(PRODUCT):
            if product_df[PRICE].isna().any():
                prices = product_df[PRICE].value_counts()
                if prices.size == 1:
                    self.update_part_of_col(product_df, PRICE,
                                            prices.index.values[0])
                else:  # TODO Handle case of multiple prices per product
                    prod_name = product_df[PRODUCT].iloc[0]
                    raise ValueError(f"Multiple prices for {prod_name}")

    def normalize_str_col(self, col_name: str, options: pd.Series) -> None:
        aberrations = self.df.loc[~self.df[col_name].isin(options), col_name]
        aberrations = aberrations.apply(self.coerce_str, args=(options, ))
        self.df.loc[aberrations.index, col_name] = aberrations

    def str2num_for_col(self, col_name: str,
                        as_type: type[NumbersIn.NumType]) -> None:
        """ _summary_

        :param df: pd.DataFrame, _description_
        :param col_name: str, _description_
        :param as_type: type[_NumType], _description_
        :return: pd.DataFrame, _description_
        """
        self.df[col_name] = NumbersIn.str_ser(self.df[col_name], as_type)

    @staticmethod
    def underscorize(string: str) -> str:
        """ Standardize column names: lowercase and underscore-separated

        :param string: str, _description_
        :return: str, _description_
        """
        return inflection.parameterize(string, separator="_")

    def update_part_of_col(self, partial_df: pd.DataFrame,
                           col_name: str, new_value: Any):
        self.df.loc[partial_df[col_name].index, col_name] = new_value
