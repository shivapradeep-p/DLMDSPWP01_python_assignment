"""
Configuration settings for the DLMDSPWP01 Programming with Python assignment.

This module stores all important project paths, required column names,
database table names, and fixed mathematical constants used across the project.
Keeping these settings in one file makes the project easier to maintain.
"""

from math import sqrt
from pathlib import Path


# ---------------------------------------------------------------------------
# Project paths
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data" / "raw"
OUTPUT_DIR = PROJECT_ROOT / "outputs"
TABLE_OUTPUT_DIR = OUTPUT_DIR / "tables"
FIGURE_OUTPUT_DIR = OUTPUT_DIR / "figures"

TRAINING_DATA_PATH = DATA_DIR / "train.csv"
IDEAL_FUNCTIONS_PATH = DATA_DIR / "ideal.csv"
TEST_DATA_PATH = DATA_DIR / "test.csv"

DATABASE_PATH = OUTPUT_DIR / "python_assignment.db"


# ---------------------------------------------------------------------------
# Required dataset columns
# ---------------------------------------------------------------------------

X_COLUMN = "x"

TRAINING_FUNCTION_COLUMNS = [f"y{i}" for i in range(1, 5)]
IDEAL_FUNCTION_COLUMNS = [f"y{i}" for i in range(1, 51)]

REQUIRED_TRAINING_COLUMNS = [X_COLUMN] + TRAINING_FUNCTION_COLUMNS
REQUIRED_IDEAL_COLUMNS = [X_COLUMN] + IDEAL_FUNCTION_COLUMNS
REQUIRED_TEST_COLUMNS = [X_COLUMN, "y"]


# ---------------------------------------------------------------------------
# Database table names
# ---------------------------------------------------------------------------

TRAINING_TABLE_NAME = "training_data"
IDEAL_TABLE_NAME = "ideal_functions"
CHOSEN_FUNCTIONS_TABLE_NAME = "chosen_functions"
MAPPED_TEST_TABLE_NAME = "mapped_test_data"


# ---------------------------------------------------------------------------
# Mathematical constants
# ---------------------------------------------------------------------------

MAPPING_THRESHOLD_FACTOR = sqrt(2)


# ---------------------------------------------------------------------------
# Output file names
# ---------------------------------------------------------------------------

CHOSEN_FUNCTIONS_OUTPUT_PATH = TABLE_OUTPUT_DIR / "chosen_functions.csv"
MAPPED_TEST_OUTPUT_PATH = TABLE_OUTPUT_DIR / "mapped_test_data.csv"

TRAINING_VS_IDEAL_FIGURE_PATH = FIGURE_OUTPUT_DIR / "training_vs_ideal.html"
MAPPED_TEST_FIGURE_PATH = FIGURE_OUTPUT_DIR / "mapped_test_data.html"
DEVIATION_FIGURE_PATH = FIGURE_OUTPUT_DIR / "deviation_plot.html"
