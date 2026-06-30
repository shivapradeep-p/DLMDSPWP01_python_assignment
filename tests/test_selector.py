"""
Unit tests for ideal-function selection logic.
"""

import pandas as pd

from src.selector import IdealFunctionSelector


def test_select_best_functions_returns_four_rows():
    """Test whether the selector returns one selected ideal function per training function."""
    x_values = [1, 2, 3]

    training_data = pd.DataFrame(
        {
            "x": x_values,
            "y1": [1, 2, 3],
            "y2": [10, 11, 12],
            "y3": [20, 21, 22],
            "y4": [30, 31, 32],
        }
    )

    ideal_data = pd.DataFrame({"x": x_values})

    ideal_data["y1"] = [1, 2, 3]
    ideal_data["y2"] = [10, 11, 12]
    ideal_data["y3"] = [20, 21, 22]
    ideal_data["y4"] = [30, 31, 32]

    for column_number in range(5, 51):
        ideal_data[f"y{column_number}"] = [999, 999, 999]

    selector = IdealFunctionSelector(training_data, ideal_data)
    chosen_functions = selector.select_best_functions()

    assert chosen_functions.shape[0] == 4
    assert list(chosen_functions["ideal_function"]) == ["y1", "y2", "y3", "y4"]
    assert all(chosen_functions["sum_squared_error"] == 0)
