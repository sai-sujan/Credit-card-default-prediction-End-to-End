"""Tests for configuration module."""
import pytest
from pathlib import Path
from config import settings, Settings


class TestSettings:
    """Test cases for Settings configuration."""

    def test_base_dir_exists(self):
        """Test that base directory is set correctly."""
        assert settings.BASE_DIR.exists()
        assert settings.BASE_DIR.is_dir()

    def test_server_config_defaults(self):
        """Test server configuration defaults."""
        assert settings.HOST == "0.0.0.0"
        assert settings.PORT == 5000
        assert isinstance(settings.DEBUG, bool)

    def test_training_paths_are_paths(self):
        """Test that training paths are Path objects."""
        assert isinstance(settings.TRAINING_BATCH_PATH, Path)
        assert isinstance(settings.TRAINING_DB_PATH, Path)
        assert isinstance(settings.TRAINING_LOGS_PATH, Path)

    def test_prediction_paths_are_paths(self):
        """Test that prediction paths are Path objects."""
        assert isinstance(settings.PREDICTION_BATCH_PATH, Path)
        assert isinstance(settings.PREDICTION_DB_PATH, Path)
        assert isinstance(settings.PREDICTION_LOGS_PATH, Path)

    def test_model_path_exists_after_init(self):
        """Test that model directory is created."""
        assert settings.MODELS_PATH.exists()
        assert settings.MODELS_PATH.is_dir()

    def test_get_training_log_path(self):
        """Test training log path generation."""
        log_path = settings.get_training_log_path("test.log")
        assert isinstance(log_path, Path)
        assert log_path.name == "test.log"
        assert "Training_Logs" in str(log_path)

    def test_get_prediction_log_path(self):
        """Test prediction log path generation."""
        log_path = settings.get_prediction_log_path("test.log")
        assert isinstance(log_path, Path)
        assert log_path.name == "test.log"
        assert "Prediction_Logs" in str(log_path)

    def test_random_state_is_int(self):
        """Test that random state is an integer."""
        assert isinstance(settings.RANDOM_STATE, int)
        assert settings.RANDOM_STATE == 42

    def test_test_size_is_float(self):
        """Test that test size is a float."""
        assert isinstance(settings.TEST_SIZE, float)
        assert 0 < settings.TEST_SIZE < 1
