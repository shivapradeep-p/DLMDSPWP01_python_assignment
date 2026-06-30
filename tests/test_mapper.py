"""
Unit tests for test-data mapping logic.
"""

import pandas as pd

from src.mapper import TestDataMapper as Mapper


def test_mapper_accepts_point_within_threshold():
    """Test whether a test point is mapped when deviation is inside the threshold."""
    test_data = pd.DataFrame(
        {
            "x": [1],
            "y": [10.5],
        }
    )

    ideal_functions = pd.DataFrame(
        {
            "x": [1],
            "y1": [10.0],
        }
    )

    chosen_functions = pd.DataFrame(
        {
            "training_function": ["y1"],
            "ideal_function": ["y1"],
            "ideal_function_number": [1],
            "sum_squared_error": [0.0],
            "max_deviation": [1.0],
            "mapping_threshold": [1.5],
        }
    )

    mapped_data = Mapper(
        test_data=test_data,
        ideal_functions=ideal_functions,
        chosen_functions=chosen_functions,
    ).map_test_data()

    assert mapped_data.shape[0] == 1
    assert mapped_data.iloc[0]["ideal_function_number"] == 1


def test_mapper_rejects_point_outside_threshold():
    """Test whether a test point is rejected when deviation is outside the threshold."""
    test_data = pd.DataFrame(
        {
            "x": [1],
            "y": [20.0],
        }
    )

    ideal_functions = pd.DataFrame(
        {
            "x": [1],
            "y1": [10.0],
        }
    )

    chosen_functions = pd.DataFrame(
        {
            "training_function": ["y1"],
            "ideal_function": ["y1"],
            "ideal_function_number": [1],
            "sum_squared_error": [0.0],
            "max_deviation": [1.0],
            "mapping_threshold": [1.5],
        }
    )

    mapped_data = Mapper(
        test_data=test_data,
        ideal_functions=ideal_functions,
        chosen_functions=chosen_functions,
    ).map_test_data()

    assert mapped_data.empty
