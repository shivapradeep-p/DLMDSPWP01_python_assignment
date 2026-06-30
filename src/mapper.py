"""
Test-data mapping module for the DLMDSPWP01 assignment.

This module maps test-data points to the selected ideal functions if the
deviation is within the allowed threshold defined by the assignment.
"""

import pandas as pd

from src.config import X_COLUMN
from src.exceptions import MappingError
from src.selector import BaseFunctionAnalyzer


class TestDataMapper(BaseFunctionAnalyzer):
    """Maps test-data points to selected ideal functions."""

    def __init__(
        self,
        test_data: pd.DataFrame,
        ideal_functions: pd.DataFrame,
        chosen_functions: pd.DataFrame,
    ) -> None:
        """Initialise the mapper with test data, ideal functions, and chosen functions."""
        self.test_data = test_data
        self.ideal_functions = ideal_functions
        self.chosen_functions = chosen_functions

    def map_test_data(self) -> pd.DataFrame:
        """
        Map each test-data point to the closest valid selected ideal function.

        A test point is accepted only if its deviation from a selected ideal
        function is less than or equal to that function's allowed mapping threshold.
        If more than one selected ideal function is valid, the one with the
        smallest deviation is chosen.
        """
        try:
            ideal_lookup = self.ideal_functions.set_index(X_COLUMN)
            mapped_rows = []

            for _, test_row in self.test_data.iterrows():
                test_x = test_row[X_COLUMN]
                test_y = test_row["y"]

                if test_x not in ideal_lookup.index:
                    continue

                valid_matches = []

                for _, chosen_row in self.chosen_functions.iterrows():
                    ideal_function = chosen_row["ideal_function"]
                    ideal_function_number = chosen_row["ideal_function_number"]
                    mapping_threshold = chosen_row["mapping_threshold"]

                    ideal_y = ideal_lookup.loc[test_x, ideal_function]
                    delta_y = abs(test_y - ideal_y)

                    if delta_y <= mapping_threshold:
                        valid_matches.append(
                            {
                                X_COLUMN: test_x,
                                "y": test_y,
                                "delta_y": float(delta_y),
                                "ideal_function_number": int(ideal_function_number),
                            }
                        )

                if valid_matches:
                    best_match = min(
                        valid_matches,
                        key=lambda row: row["delta_y"],
                    )
                    mapped_rows.append(best_match)

            return pd.DataFrame(
                mapped_rows,
                columns=[X_COLUMN, "y", "delta_y", "ideal_function_number"],
            )

        except Exception as error:
            raise MappingError(
                "Failed to map test data to ideal functions.") from error
