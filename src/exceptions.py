"""
Custom exceptions for the DLMDSPWP01 Programming with Python assignment.

These exceptions make error handling clearer by separating different
types of problems, such as data loading, schema validation, database
operations, function selection, and test data mapping.
"""


class AssignmentError(Exception):
    """Base exception for all custom assignment-related errors."""


class DataLoadingError(AssignmentError):
    """Raised when a dataset cannot be loaded successfully."""


class SchemaValidationError(AssignmentError):
    """Raised when a dataset does not contain the expected columns or values."""


class DatabaseOperationError(AssignmentError):
    """Raised when a database operation fails."""


class FunctionSelectionError(AssignmentError):
    """Raised when the ideal-function selection process fails."""


class MappingError(AssignmentError):
    """Raised when test-data mapping fails."""
