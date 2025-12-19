"""
Custom exceptions for Credit Card Default Prediction application.

This module defines a hierarchy of custom exceptions for better error handling
and debugging. Each exception provides specific context about what went wrong.
"""
from typing import Optional


class CCDPException(Exception):
    """
    Base exception for all Credit Card Default Prediction errors.

    All custom exceptions in this application should inherit from this class.
    This allows catching all application-specific errors with a single except block.

    Args:
        message: Human-readable error description
        details: Optional dict with additional error context
    """

    def __init__(self, message: str, details: Optional[dict] = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)

    def __str__(self) -> str:
        if self.details:
            details_str = ", ".join(f"{k}={v}" for k, v in self.details.items())
            return f"{self.message} ({details_str})"
        return self.message


class DataValidationError(CCDPException):
    """
    Raised when data validation fails.

    Examples:
        - Invalid file format
        - Missing required columns
        - Wrong data types
        - Schema mismatch
    """
    pass


class DataIngestionError(CCDPException):
    """
    Raised when data ingestion fails.

    Examples:
        - File not found
        - Unable to read file
        - Corrupted data
        - Permission denied
    """
    pass


class DataPreprocessingError(CCDPException):
    """
    Raised when data preprocessing fails.

    Examples:
        - Imputation failure
        - Scaling failure
        - Encoding failure
        - Invalid transformation
    """
    pass


class ModelTrainingError(CCDPException):
    """
    Raised when model training fails.

    Examples:
        - Insufficient data
        - Invalid hyperparameters
        - Training timeout
        - Convergence failure
    """
    pass


class ModelPredictionError(CCDPException):
    """
    Raised when model prediction fails.

    Examples:
        - Model not found
        - Invalid input features
        - Prediction error
        - Model version mismatch
    """
    pass


class DatabaseError(CCDPException):
    """
    Raised when database operations fail.

    Examples:
        - Connection failure
        - Query execution error
        - Table creation failure
        - Data insertion error
    """
    pass


class FileOperationError(CCDPException):
    """
    Raised when file operations fail.

    Examples:
        - File save error
        - File load error
        - Directory creation error
        - File deletion error
    """
    pass


class ConfigurationError(CCDPException):
    """
    Raised when configuration is invalid or missing.

    Examples:
        - Missing environment variable
        - Invalid configuration value
        - Configuration file not found
    """
    pass


class ClusteringError(CCDPException):
    """
    Raised when clustering operations fail.

    Examples:
        - Invalid number of clusters
        - Clustering convergence failure
        - Empty cluster created
    """
    pass


class SchemaError(DataValidationError):
    """
    Raised when schema validation fails.

    Examples:
        - Schema file not found
        - Invalid schema format
        - Schema version mismatch
    """
    pass


# Convenience exception with context manager support
class ErrorContext:
    """
    Context manager for adding context to exceptions.

    Usage:
        with ErrorContext("preprocessing data", file="train.csv"):
            preprocess_data()

    This will wrap any exception with additional context.
    """

    def __init__(self, operation: str, **context):
        self.operation = operation
        self.context = context

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type and issubclass(exc_type, CCDPException):
            # Add context to existing CCDP exception
            exc_val.details.update({
                'operation': self.operation,
                **self.context
            })
        elif exc_type:
            # Wrap other exceptions in CCDPException
            raise CCDPException(
                f"Error during {self.operation}: {str(exc_val)}",
                details=self.context
            ) from exc_val
        return False
