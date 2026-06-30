"""
Unit tests for database operations.
"""

import pandas as pd

from src.database import DatabaseManager


def test_database_saves_and_lists_table(tmp_path):
    """Test whether a DataFrame can be saved into a temporary SQLite database."""
    database_path = tmp_path / "test_assignment.db"
    database_manager = DatabaseManager(database_path=database_path)

    dataframe = pd.DataFrame(
        {
            "x": [1, 2, 3],
            "y1": [4, 5, 6],
        }
    )

    database_manager.save_dataframe(dataframe, "example_table")

    tables = database_manager.list_tables()

    assert "example_table" in tables
