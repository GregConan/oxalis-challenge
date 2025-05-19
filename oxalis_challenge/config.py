#!/usr/bin/env python3
# coding: utf-8

"""
Oxalis Challenge: Configuration details
Greg Conan: gregmconan@gmail.com
Created: 2025-05-17
Updated: 2024-05-17
"""
# Import standard libraries
import os

# PostgreSQLAlchemy DB details
SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", "")
