"""
Ideal-function selection module for the DLMDSPWP01 assignment.

This module selects the best-fitting ideal function for each of the four
training functions by minimizing the sum of squared y-deviations.
"""

import pandas as pd

from src.config import (
    X_COLUMN,
    TRAINING_FUNCTION_COLUMNS,
    IDEAL_FUNCTION_COLUMNS,
    MAPPING_THRESHOLD_FACTOR,
)
from src.exceptions import FunctionSelectionError


class BaseFunctionAnalyzer:
    """Base class containing shared functionality for function analysis."""

    @staticmethod
    def calculate_absolute_deviation(
        observed_values: pd.Series,
        ideal_values: pd.Series,
    ) -> pd.Series:
        """Calculate absolute deviation between observed and ideal y-values."""
        return (observed_values - ideal_values).abs()

    @staticmethod
    def calculate_sum_squared_error(
        observed_values: pd.Series,
        ideal_values: pd.Series,
    ) -> float:
        """Calculate the sum of squared errors between two functions."""
        deviations = observed_values - ideal_values
        return float((deviations**2).sum())


class IdealFunctionSelector(BaseFunctionAnalyzer):
    """Selects the best ideal functions for the four training functions."""

    def __init__(
        self,
        training_data: pd.DataFrame,
        ideal_functions: pd.DataFrame,
    ) -> None:
        """Initialise the selector with training and ideal-function datasets."""
        self.training_data = training_data
        self.ideal_functions = ideal_functions

    def _get_aligned_data(self) -> pd.DataFrame:
        """Merge training data and ideal functions using the x-column."""
        try:
            training_renamed = self.training_data.rename(
                columns={
                    column: f"{column}_training"
                    for column in TRAINING_FUNCTION_COLUMNS
                }
            )

            ideal_renamed = self.ideal_functions.rename(
                columns={
                    column: f"{column}_ideal"
                    for column in IDEAL_FUNCTION_COLUMNS
                }
            )

            return pd.merge(
                training_renamed,
                ideal_renamed,
                on=X_COLUMN,
                how="inner",
            )

        except Exception as error:
            raise FunctionSelectionError(
                "Failed to align training data with ideal functions."
            ) from error

    def select_best_functions(self) -> pd.DataFrame:
        """
        Select the best-fitting ideal function for each training function.

        For each training function, all 50 ideal functions are compared.
        The ideal function with the lowest sum of squared errors is selected.
        """
        try:
            aligned_data = self._get_aligned_data()
            selection_results = []

            for training_column in TRAINING_FUNCTION_COLUMNS:
                training_values = aligned_data[f"{training_column}_training"]

                best_ideal_function = None
                lowest_sse = float("inf")
                best_max_deviation = None

                for ideal_column in IDEAL_FUNCTION_COLUMNS:
                    ideal_values = aligned_data[f"{ideal_column}_ideal"]

                    sse = self.calculate_sum_squared_error(
                        training_values,
                        ideal_values,
                    )

                    if sse < lowest_sse:
                        deviations = self.calculate_absolute_deviation(
                            training_values,
                            ideal_values,
                        )

                        lowest_sse = sse
                        best_ideal_function = ideal_column
                        best_max_deviation = float(deviations.max())

                selection_results.append(
                    {
                        "training_function": training_column,
                        "ideal_function": best_ideal_function,
                        "ideal_function_number": int(
                            best_ideal_function.replace("y", "")
                        ),
                        "sum_squared_error": lowest_sse,
                        "max_deviation": best_max_deviation,
                        "mapping_threshold": best_max_deviation
                        * MAPPING_THRESHOLD_FACTOR,
                    }
                )

            return pd.DataFrame(selection_results)

        except Exception as error:
            if isinstance(error, FunctionSelectionError):
                raise

            raise FunctionSelectionError(
                "Failed to select the best ideal functions."
            ) from error
