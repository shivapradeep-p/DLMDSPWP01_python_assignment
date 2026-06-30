"""
Visualisation module for the DLMDSPWP01 assignment.

This module creates Bokeh visualisations for the training data, selected
ideal functions, mapped test data, and deviation values.
"""

import pandas as pd
from bokeh.io import output_file, save
from bokeh.models import HoverTool
from bokeh.palettes import Category10
from bokeh.plotting import figure

from src.config import (
    X_COLUMN,
    TRAINING_FUNCTION_COLUMNS,
    TRAINING_VS_IDEAL_FIGURE_PATH,
    MAPPED_TEST_FIGURE_PATH,
    DEVIATION_FIGURE_PATH,
)
from src.exceptions import AssignmentError


class BokehVisualizer:
    """Creates Bokeh visualisations for assignment outputs."""

    def __init__(
        self,
        training_data: pd.DataFrame,
        ideal_functions: pd.DataFrame,
        chosen_functions: pd.DataFrame,
        mapped_test_data: pd.DataFrame,
    ) -> None:
        """Initialise the visualizer with all required datasets."""
        self.training_data = training_data
        self.ideal_functions = ideal_functions
        self.chosen_functions = chosen_functions
        self.mapped_test_data = mapped_test_data

    def create_training_vs_ideal_plot(self) -> None:
        """Create a plot comparing training functions with selected ideal functions."""
        try:
            output_file(TRAINING_VS_IDEAL_FIGURE_PATH)

            plot = figure(
                title="Training Functions Compared with Selected Ideal Functions",
                x_axis_label="x",
                y_axis_label="y",
                width=1000,
                height=600,
                tools="pan,wheel_zoom,box_zoom,reset,save",
            )

            colors = Category10[10]

            for index, row in self.chosen_functions.iterrows():
                training_function = row["training_function"]
                ideal_function = row["ideal_function"]
                color = colors[index]

                plot.line(
                    self.training_data[X_COLUMN],
                    self.training_data[training_function],
                    legend_label=f"Training {training_function}",
                    line_width=2,
                    color=color,
                )

                plot.line(
                    self.ideal_functions[X_COLUMN],
                    self.ideal_functions[ideal_function],
                    legend_label=f"Selected Ideal {ideal_function}",
                    line_width=2,
                    line_dash="dashed",
                    color=color,
                )

            plot.legend.click_policy = "hide"
            plot.legend.location = "top_right"
            plot.add_tools(
                HoverTool(
                    tooltips=[
                        ("x", "$x"),
                        ("y", "$y"),
                    ]
                )
            )

            save(plot)

        except Exception as error:
            raise AssignmentError(
                "Failed to create training vs ideal function plot."
            ) from error

    def create_mapped_test_plot(self) -> None:
        """Create a scatter plot of mapped test-data points."""
        try:
            output_file(MAPPED_TEST_FIGURE_PATH)

            plot = figure(
                title="Mapped Test Data Assigned to Ideal Functions",
                x_axis_label="x",
                y_axis_label="y",
                width=1000,
                height=600,
                tools="pan,wheel_zoom,box_zoom,reset,save",
            )

            ideal_numbers = sorted(
                self.mapped_test_data["ideal_function_number"].unique()
            )
            colors = Category10[10]

            for index, ideal_number in enumerate(ideal_numbers):
                subset = self.mapped_test_data[
                    self.mapped_test_data["ideal_function_number"] == ideal_number
                ]

                plot.scatter(
                    subset[X_COLUMN],
                    subset["y"],
                    size=8,
                    color=colors[index],
                    alpha=0.8,
                    legend_label=f"Ideal Function {ideal_number}",
                )

            plot.legend.click_policy = "hide"
            plot.legend.location = "top_right"
            plot.add_tools(
                HoverTool(
                    tooltips=[
                        ("x", "$x"),
                        ("y", "$y"),
                    ]
                )
            )

            save(plot)

        except Exception as error:
            raise AssignmentError(
                "Failed to create mapped test-data plot.") from error

    def create_deviation_plot(self) -> None:
        """Create a plot showing deviation values for mapped test-data points."""
        try:
            output_file(DEVIATION_FIGURE_PATH)

            deviation_data = self.mapped_test_data.reset_index(
                drop=True).copy()
            deviation_data["point_index"] = deviation_data.index + 1

            plot = figure(
                title="Deviation Values of Mapped Test Data",
                x_axis_label="Mapped test point index",
                y_axis_label="Delta y",
                width=1000,
                height=600,
                tools="pan,wheel_zoom,box_zoom,reset,save",
            )

            plot.scatter(
                deviation_data["point_index"],
                deviation_data["delta_y"],
                size=8,
                color=Category10[10][0],
                alpha=0.8,
                legend_label="Delta y",
            )

            plot.line(
                deviation_data["point_index"],
                deviation_data["delta_y"],
                line_width=2,
                color=Category10[10][0],
                legend_label="Deviation trend",
            )

            plot.legend.click_policy = "hide"
            plot.legend.location = "top_right"
            plot.add_tools(
                HoverTool(
                    tooltips=[
                        ("Point", "@x"),
                        ("Delta y", "@y"),
                    ]
                )
            )

            save(plot)

        except Exception as error:
            raise AssignmentError(
                "Failed to create deviation plot.") from error

    def create_all_plots(self) -> None:
        """Create all visualisations required for the assignment."""
        self.create_training_vs_ideal_plot()
        self.create_mapped_test_plot()
        self.create_deviation_plot()
