"""
Database management module for the DLMDSPWP01 assignment.

This module provides a DatabaseManager class that creates and manages
the SQLite database used to store training data, ideal functions,
chosen functions, and mapped test data.
"""

from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, inspect
from sqlalchemy.engine import Engine

from src.config import (
    DATABASE_PATH,
    OUTPUT_DIR,
    TABLE_OUTPUT_DIR,
    FIGURE_OUTPUT_DIR,
    TRAINING_TABLE_NAME,
    IDEAL_TABLE_NAME,
    CHOSEN_FUNCTIONS_TABLE_NAME,
    MAPPED_TEST_TABLE_NAME,
)
from src.exceptions import DatabaseOperationError


class DatabaseManager:
    """Creates and manages the SQLite database for the assignment."""

    def __init__(self, database_path: Path = DATABASE_PATH) -> None:
        """Initialise the database manager with a SQLite database path."""
        self.database_path = database_path
        self.engine = self._create_engine()

    def _create_engine(self) -> Engine:
        """Create a SQLAlchemy engine for the SQLite database."""
        try:
            OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
            TABLE_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
            FIGURE_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

            database_url = f"sqlite:///{self.database_path}"
            return create_engine(database_url)

        except Exception as error:
            raise DatabaseOperationError(
                f"Failed to create database engine for {self.database_path}"
            ) from error

    def save_dataframe(
        self,
        dataframe: pd.DataFrame,
        table_name: str,
        if_exists: str = "replace",
    ) -> None:
        """Save a Pandas DataFrame into a SQLite database table."""
        try:
            dataframe.to_sql(
                name=table_name,
                con=self.engine,
                if_exists=if_exists,
                index=False,
            )

        except Exception as error:
            raise DatabaseOperationError(
                f"Failed to save DataFrame to table '{table_name}'."
            ) from error

    def load_table(self, table_name: str) -> pd.DataFrame:
        """Load a SQLite database table as a Pandas DataFrame."""
        try:
            return pd.read_sql_table(table_name, con=self.engine)

        except Exception as error:
            raise DatabaseOperationError(
                f"Failed to load table '{table_name}' from the database."
            ) from error

    def list_tables(self) -> list[str]:
        """Return a list of all table names currently stored in the database."""
        try:
            inspector = inspect(self.engine)
            return inspector.get_table_names()

        except Exception as error:
            raise DatabaseOperationError(
                "Failed to inspect database tables."
            ) from error

    def save_initial_datasets(
        self,
        training_data: pd.DataFrame,
        ideal_functions: pd.DataFrame,
    ) -> None:
        """Save the original training and ideal-function datasets."""
        self.save_dataframe(training_data, TRAINING_TABLE_NAME)
        self.save_dataframe(ideal_functions, IDEAL_TABLE_NAME)

    def save_chosen_functions(self, chosen_functions: pd.DataFrame) -> None:
        """Save the selected ideal-function results."""
        self.save_dataframe(chosen_functions, CHOSEN_FUNCTIONS_TABLE_NAME)

    def save_mapped_test_data(self, mapped_test_data: pd.DataFrame) -> None:
        """Save the mapped test-data results."""
        self.save_dataframe(mapped_test_data, MAPPED_TEST_TABLE_NAME)
