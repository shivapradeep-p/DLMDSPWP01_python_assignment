# DLMDSPWP01 Programming with Python Assignment

## Project Overview

This project implements a Python-based solution for the DLMDSPWP01 Programming with Python written assignment.

The program loads training data, ideal-function data, and test data from CSV files. It selects the best-fitting ideal function for each of the four training functions using the least-square criterion. It then maps test-data points to the selected ideal functions if the deviation satisfies the required threshold rule.

The project uses:

- Python
- Pandas
- SQLAlchemy
- SQLite
- Bokeh
- Pytest

## Project Structure

```text
DLMDSPWP01_python_assignment/
│
├── data/
│   └── raw/
│       ├── train.csv
│       ├── ideal.csv
│       └── test.csv
│
├── src/
│   ├── config.py
│   ├── exceptions.py
│   ├── data_loader.py
│   ├── database.py
│   ├── selector.py
│   ├── mapper.py
│   ├── visualizer.py
│   └── main.py
│
├── tests/
│   ├── test_data_loader.py
│   ├── test_database.py
│   ├── test_mapper.py
│   └── test_selector.py
│
├── outputs/
│   ├── figures/
│   └── tables/
│
├── run.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Dataset Files

The required dataset files must be placed in:

```text
data/raw/
```

Required files:

```text
train.csv
ideal.csv
test.csv
```

The raw input data is not included in this repository/package unless required by the examiner or submission platform.

## How to Set Up the Project

Create and activate a virtual environment:

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

Install required packages:

```bash
pip install -r requirements.txt
```

## How to Run the Program

Run the complete assignment pipeline:

```bash
python run.py
```

This will:

- load and validate the datasets;
- create a SQLite database;
- save the training and ideal-function data;
- select the four best-fitting ideal functions;
- map valid test-data points;
- save output tables;
- generate Bokeh visualisations.

## Generated Outputs

After running the program, the following outputs are generated:

```text
outputs/python_assignment.db
outputs/tables/chosen_functions.csv
outputs/tables/mapped_test_data.csv
outputs/figures/training_vs_ideal.html
outputs/figures/mapped_test_data.html
outputs/figures/deviation_plot.html
```

## How to Run Unit Tests

Run:

```bash
pytest
```

or:

```bash
python -m pytest
```

The tests validate important parts of the project, including data loading, schema validation, ideal-function selection, test-data mapping, and database operations.

## Notes

The full source code is also intended to be included in the appendix of the written assignment, as required by the task instructions.
