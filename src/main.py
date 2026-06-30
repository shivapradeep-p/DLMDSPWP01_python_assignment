"""
Main execution pipeline for the DLMDSPWP01 Programming with Python assignment.

This module connects all project components: data loading, database storage,
ideal-function selection, test-data mapping, CSV export, and visualisation.
"""

from src.config import (
    CHOSEN_FUNCTIONS_OUTPUT_PATH,
    MAPPED_TEST_OUTPUT_PATH,
    TABLE_OUTPUT_DIR,
)
from src.data_loader import CSVDataLoader
from src.database import DatabaseManager
from src.mapper import TestDataMapper
from src.selector import IdealFunctionSelector
from src.visualizer import BokehVisualizer


class AssignmentPipeline:
    """Runs the complete assignment workflow from input data to final outputs."""

    def __init__(self) -> None:
        """Initialise the pipeline with data loader and database manager."""
        self.data_loader = CSVDataLoader()
        self.database_manager = DatabaseManager()

    def run(self) -> None:
        """Execute the complete assignment pipeline."""
        print("Starting DLMDSPWP01 Python assignment pipeline...")

        TABLE_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        training_data, ideal_functions, test_data = self.data_loader.load_all_data()
        print("Datasets loaded successfully.")
        print(f"Training data shape: {training_data.shape}")
        print(f"Ideal functions shape: {ideal_functions.shape}")
        print(f"Test data shape: {test_data.shape}")

        self.database_manager.save_initial_datasets(
            training_data=training_data,
            ideal_functions=ideal_functions,
        )
        print("Training data and ideal functions saved to SQLite database.")

        selector = IdealFunctionSelector(
            training_data=training_data,
            ideal_functions=ideal_functions,
        )
        chosen_functions = selector.select_best_functions()

        self.database_manager.save_chosen_functions(chosen_functions)
        chosen_functions.to_csv(CHOSEN_FUNCTIONS_OUTPUT_PATH, index=False)
        print("Best ideal functions selected and saved.")

        mapper = TestDataMapper(
            test_data=test_data,
            ideal_functions=ideal_functions,
            chosen_functions=chosen_functions,
        )
        mapped_test_data = mapper.map_test_data()

        self.database_manager.save_mapped_test_data(mapped_test_data)
        mapped_test_data.to_csv(MAPPED_TEST_OUTPUT_PATH, index=False)
        print("Test data mapped and saved.")

        visualizer = BokehVisualizer(
            training_data=training_data,
            ideal_functions=ideal_functions,
            chosen_functions=chosen_functions,
            mapped_test_data=mapped_test_data,
        )
        visualizer.create_all_plots()
        print("Bokeh visualisations created successfully.")

        print("\nPipeline completed successfully.")
        print("\nSelected ideal functions:")
        print(chosen_functions)

        print("\nMapped test-data preview:")
        print(mapped_test_data.head())

        print("\nMapped test-data shape:")
        print(mapped_test_data.shape)

        print("\nDatabase tables:")
        print(self.database_manager.list_tables())


def main() -> None:
    """Run the assignment pipeline."""
    pipeline = AssignmentPipeline()
    pipeline.run()


if __name__ == "__main__":
    main()
