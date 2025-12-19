"""
Central configuration management for Credit Card Default Prediction.

This module provides a centralized configuration system using environment variables
and sensible defaults for all application settings.
"""
import os
from pathlib import Path
from typing import Optional


class Settings:
    """Application settings with environment variable support."""

    # Base directories
    BASE_DIR: Path = Path(__file__).resolve().parent.parent

    # Server configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 5000))
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    # Training paths
    TRAINING_BATCH_PATH: Path = BASE_DIR / os.getenv("TRAINING_BATCH_PATH", "Training_Batch_Files")
    TRAINING_DB_PATH: Path = BASE_DIR / os.getenv("TRAINING_DB_PATH", "Training_Database")
    TRAINING_LOGS_PATH: Path = BASE_DIR / os.getenv("TRAINING_LOGS_PATH", "Training_Logs")
    TRAINING_ARCHIVE_PATH: Path = BASE_DIR / "Training_Archive"
    TRAINING_GOOD_RAW_PATH: Path = TRAINING_BATCH_PATH / "Good_Raw"
    TRAINING_BAD_RAW_PATH: Path = TRAINING_BATCH_PATH / "Bad_Raw"

    # Prediction paths
    PREDICTION_BATCH_PATH: Path = BASE_DIR / os.getenv("PREDICTION_BATCH_PATH", "Prediction_Batch_files")
    PREDICTION_DB_PATH: Path = BASE_DIR / os.getenv("PREDICTION_DB_PATH", "Prediction_Database")
    PREDICTION_LOGS_PATH: Path = BASE_DIR / os.getenv("PREDICTION_LOGS_PATH", "Prediction_Logs")
    PREDICTION_ARCHIVE_PATH: Path = BASE_DIR / "Prediction_Archive"
    PREDICTION_GOOD_RAW_PATH: Path = PREDICTION_BATCH_PATH / "Good_Raw"
    PREDICTION_BAD_RAW_PATH: Path = PREDICTION_BATCH_PATH / "Bad_Raw"
    PREDICTION_OUTPUT_PATH: Path = BASE_DIR / "Prediction_Output_File"

    # Model paths
    MODELS_PATH: Path = BASE_DIR / os.getenv("MODELS_PATH", "models")

    # Data preprocessing
    PREPROCESSING_DATA_PATH: Path = BASE_DIR / "preprocessing_data"

    # Schema files
    TRAINING_SCHEMA_PATH: Path = BASE_DIR / "schema_training.json"
    PREDICTION_SCHEMA_PATH: Path = BASE_DIR / "schema_prediction.json"

    # Database configuration
    TRAINING_DB_NAME: str = os.getenv("TRAINING_DB_NAME", "Training.db")
    PREDICTION_DB_NAME: str = os.getenv("PREDICTION_DB_NAME", "Prediction.db")
    TRAINING_TABLE_NAME: str = "Good_Raw_Data"
    PREDICTION_TABLE_NAME: str = "Good_Raw_Data"

    # Logging configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"

    # ML Model parameters
    RANDOM_STATE: int = int(os.getenv("RANDOM_STATE", 42))
    TEST_SIZE: float = float(os.getenv("TEST_SIZE", 0.33))
    N_CLUSTERS_MIN: int = 1
    N_CLUSTERS_MAX: int = 11

    # API Configuration
    MAX_CONTENT_LENGTH: int = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS: set = {'.csv'}

    @classmethod
    def create_directories(cls) -> None:
        """Create all necessary directories if they don't exist."""
        directories = [
            cls.TRAINING_BATCH_PATH,
            cls.TRAINING_DB_PATH,
            cls.TRAINING_LOGS_PATH,
            cls.TRAINING_ARCHIVE_PATH,
            cls.TRAINING_GOOD_RAW_PATH,
            cls.TRAINING_BAD_RAW_PATH,
            cls.PREDICTION_BATCH_PATH,
            cls.PREDICTION_DB_PATH,
            cls.PREDICTION_LOGS_PATH,
            cls.PREDICTION_ARCHIVE_PATH,
            cls.PREDICTION_GOOD_RAW_PATH,
            cls.PREDICTION_BAD_RAW_PATH,
            cls.PREDICTION_OUTPUT_PATH,
            cls.MODELS_PATH,
            cls.PREPROCESSING_DATA_PATH,
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

    @classmethod
    def get_training_log_path(cls, log_name: str) -> Path:
        """Get the full path for a training log file."""
        return cls.TRAINING_LOGS_PATH / log_name

    @classmethod
    def get_prediction_log_path(cls, log_name: str) -> Path:
        """Get the full path for a prediction log file."""
        return cls.PREDICTION_LOGS_PATH / log_name

    @classmethod
    def get_training_db_path(cls) -> Path:
        """Get the full path for the training database."""
        return cls.TRAINING_DB_PATH / cls.TRAINING_DB_NAME

    @classmethod
    def get_prediction_db_path(cls) -> Path:
        """Get the full path for the prediction database."""
        return cls.PREDICTION_DB_PATH / cls.PREDICTION_DB_NAME


# Create directories on module import
Settings.create_directories()
