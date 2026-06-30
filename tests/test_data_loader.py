"""
Unit tests for the CSVDataLoader class.
"""

import pandas as pd
import pytest

from src.data_loader import CSVDataLoader
from src.exceptions import SchemaValidationError


def test_load_all_data_returns_expected_shapes():
    """Test whether all real datasets load with the expected shapes."""
    loader = CSVDataLoader()

    training_data, ideal_functions, test_data = loader.load_all_data()

    assert training_data.shape == (400, 5)
    assert ideal_functions.shape == (400, 51)
    assert test_data.shape == (100, 2)


def test_validate_columns_raises_error_for_missing_column():
    """Test whether missing required columns are detected."""
    dataframe = pd.DataFrame(
        {
            "x": [1, 2, 3],
            "y1": [1, 2, 3],
        }
    )

    with pytest.raises(SchemaValidationError):
        CSVDataLoader.validate_columns(
            dataframe=dataframe,
            required_columns=["x", "y1", "y2"],
            dataset_name="Example dataset",
        )
