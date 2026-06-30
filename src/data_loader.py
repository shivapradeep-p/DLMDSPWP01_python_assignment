"""
Data loading and validation module for the DLMDSPWP01 assignment.

This module provides a CSVDataLoader class that loads the training,
ideal-function, and test datasets. It also validates whether the required
columns exist and whether the relevant values are numeric.
"""

from pathlib import Path
from typing import Iterable

import pandas as pd

from src.config import (
    TRAINING_DATA_PATH,
    IDEAL_FUNCTIONS_PATH,
    TEST_DATA_PATH,
    REQUIRED_TRAINING_COLUMNS,
    REQUIRED_IDEAL_COLUMNS,
    REQUIRED_TEST_COLUMNS,
)
from src.exceptions import DataLoadingError, SchemaValidationError


class CSVDataLoader:
    """Loads and validates all CSV datasets required for the assignment."""

    def __init__(
        self,
        training_path: Path = TRAINING_DATA_PATH,
        ideal_path: Path = IDEAL_FUNCTIONS_PATH,
        test_path: Path = TEST_DATA_PATH,
    ) -> None:
        """Initialise the loader with paths to the required CSV files."""
        self.training_path = training_path
        self.ideal_path = ideal_path
        self.test_path = test_path

    def load_csv(self, file_path: Path, dataset_name: str) -> pd.DataFrame:
        """Load a CSV file as a Pandas DataFrame."""
        try:
            if not file_path.exists():
                raise DataLoadingError(
                    f"{dataset_name} file not found: {file_path}")

            return pd.read_csv(file_path)

        except DataLoadingError:
            raise

        except Exception as error:
            raise DataLoadingError(
                f"Failed to load {dataset_name} from {file_path}"
            ) from error

    @staticmethod
    def validate_columns(
        dataframe: pd.DataFrame,
        required_columns: Iterable[str],
        dataset_name: str,
    ) -> None:
        """Validate whether a dataset contains all required columns."""
        missing_columns = [
            column for column in required_columns if column not in dataframe.columns
        ]

        if missing_columns:
            raise SchemaValidationError(
                f"{dataset_name} is missing required columns: {missing_columns}"
            )

    @staticmethod
    def validate_numeric_values(
        dataframe: pd.DataFrame,
        columns: Iterable[str],
        dataset_name: str,
    ) -> pd.DataFrame:
        """Validate and convert selected columns to numeric values."""
        validated_dataframe = dataframe.copy()

        try:
            for column in columns:
                validated_dataframe[column] = pd.to_numeric(
                    validated_dataframe[column],
                    errors="raise",
                )

        except Exception as error:
            raise SchemaValidationError(
                f"{dataset_name} contains non-numeric values."
            ) from error

        if validated_dataframe[list(columns)].isnull().any().any():
            raise SchemaValidationError(
                f"{dataset_name} contains missing numeric values."
            )

        return validated_dataframe

    def load_training_data(self) -> pd.DataFrame:
        """Load and validate the training dataset."""
        training_data = self.load_csv(self.training_path, "Training data")
        self.validate_columns(
            training_data,
            REQUIRED_TRAINING_COLUMNS,
            "Training data",
        )

        training_data = training_data[REQUIRED_TRAINING_COLUMNS]
        return self.validate_numeric_values(
            training_data,
            REQUIRED_TRAINING_COLUMNS,
            "Training data",
        )

    def load_ideal_functions(self) -> pd.DataFrame:
        """Load and validate the ideal-functions dataset."""
        ideal_functions = self.load_csv(self.ideal_path, "Ideal functions")
        self.validate_columns(
            ideal_functions,
            REQUIRED_IDEAL_COLUMNS,
            "Ideal functions",
        )

        ideal_functions = ideal_functions[REQUIRED_IDEAL_COLUMNS]
        return self.validate_numeric_values(
            ideal_functions,
            REQUIRED_IDEAL_COLUMNS,
            "Ideal functions",
        )

    def load_test_data(self) -> pd.DataFrame:
        """Load and validate the test dataset."""
        test_data = self.load_csv(self.test_path, "Test data")
        self.validate_columns(
            test_data,
            REQUIRED_TEST_COLUMNS,
            "Test data",
        )

        test_data = test_data[REQUIRED_TEST_COLUMNS]
        return self.validate_numeric_values(
            test_data,
            REQUIRED_TEST_COLUMNS,
            "Test data",
        )

    def load_all_data(self) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Load and validate training, ideal-function, and test datasets."""
        training_data = self.load_training_data()
        ideal_functions = self.load_ideal_functions()
        test_data = self.load_test_data()

        return training_data, ideal_functions, test_data
