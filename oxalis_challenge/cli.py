#!/usr/bin/env python3

"""
Oxalis Challenge: Command-line input functions/classes
Greg Conan: gregmconan@gmail.com
Created: 2025-05-17
Updated: 2025-05-17
"""
# Import standard libraries
import argparse
import os
from typing import Any


def get_cli_args() -> dict[str, Any]:
    parser = argparse.ArgumentParser()
    parser.add_argument("sales_data_file", type=valid_readable_file)
    return vars(parser.parse_args())


def valid_readable_file(path: Any) -> str:
    """ Throw exception unless parameter is a valid readable filepath string.
        Use this, not argparse.FileType('r') which leaves an open file handle.

    :param path: Any, input argument to check whether it is a valid filepath
    :raises argparse.ArgumentTypeError: if path isn't a valid filepath.
    :return: str, a valid filepath
    """
    try:
        assert os.access(path, os.R_OK)
        return os.path.abspath(path)
    except (argparse.ArgumentTypeError, AssertionError, OSError,
            TypeError, ValueError):
        raise argparse.ArgumentTypeError(f"Cannot read file at '{path}'")
