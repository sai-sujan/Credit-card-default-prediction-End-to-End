"""Tests for custom exceptions module."""
import pytest
from utils.exceptions import (
    CCDPException,
    DataValidationError,
    DataIngestionError,
    DataPreprocessingError,
    ModelTrainingError,
    ModelPredictionError,
    DatabaseError,
    FileOperationError,
    ConfigurationError,
    ErrorContext
)


class TestCustomExceptions:
    """Test cases for custom exception classes."""

    def test_base_exception_with_message(self):
        """Test CCDPException with just a message."""
        exc = CCDPException("Test error")
        assert str(exc) == "Test error"
        assert exc.message == "Test error"
        assert exc.details == {}

    def test_base_exception_with_details(self):
        """Test CCDPException with message and details."""
        exc = CCDPException("Test error", details={"key": "value"})
        assert "Test error" in str(exc)
        assert "key=value" in str(exc)
        assert exc.details == {"key": "value"}

    def test_data_validation_error_inheritance(self):
        """Test DataValidationError inherits from CCDPException."""
        exc = DataValidationError("Invalid data")
        assert isinstance(exc, CCDPException)
        assert isinstance(exc, DataValidationError)

    def test_data_ingestion_error(self):
        """Test DataIngestionError."""
        exc = DataIngestionError("Cannot read file", details={"file": "test.csv"})
        assert "Cannot read file" in str(exc)
        assert exc.details["file"] == "test.csv"

    def test_data_preprocessing_error(self):
        """Test DataPreprocessingError."""
        exc = DataPreprocessingError("Imputation failed")
        assert str(exc) == "Imputation failed"

    def test_model_training_error(self):
        """Test ModelTrainingError."""
        exc = ModelTrainingError("Training failed", details={"epoch": 10})
        assert "Training failed" in str(exc)

    def test_model_prediction_error(self):
        """Test ModelPredictionError."""
        exc = ModelPredictionError("Model not found")
        assert str(exc) == "Model not found"

    def test_database_error(self):
        """Test DatabaseError."""
        exc = DatabaseError("Connection failed")
        assert str(exc) == "Connection failed"

    def test_file_operation_error(self):
        """Test FileOperationError."""
        exc = FileOperationError("Save failed")
        assert str(exc) == "Save failed"

    def test_configuration_error(self):
        """Test ConfigurationError."""
        exc = ConfigurationError("Missing env var")
        assert str(exc) == "Missing env var"


class TestErrorContext:
    """Test cases for ErrorContext context manager."""

    def test_error_context_with_ccdp_exception(self):
        """Test ErrorContext wraps CCDPException with additional context."""
        with pytest.raises(DataValidationError) as exc_info:
            with ErrorContext("validating data", file="test.csv"):
                raise DataValidationError("Invalid schema")

        exc = exc_info.value
        assert exc.details["operation"] == "validating data"
        assert exc.details["file"] == "test.csv"

    def test_error_context_with_standard_exception(self):
        """Test ErrorContext wraps standard exceptions in CCDPException."""
        with pytest.raises(CCDPException) as exc_info:
            with ErrorContext("processing data", record_id=123):
                raise ValueError("Invalid value")

        exc = exc_info.value
        assert "Error during processing data" in str(exc)
        assert exc.details["record_id"] == 123

    def test_error_context_no_exception(self):
        """Test ErrorContext with no exception raised."""
        with ErrorContext("normal operation", status="ok"):
            pass  # No exception should be fine
