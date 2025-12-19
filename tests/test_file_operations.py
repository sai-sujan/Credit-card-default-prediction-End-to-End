"""Tests for file operations module."""
import pytest
import joblib
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
import shutil

from file_operations.file_methods import File_Operation
from utils.exceptions import FileOperationError, ModelPredictionError
from config import settings


@pytest.fixture
def file_ops():
    """Fixture for File_Operation instance."""
    return File_Operation()


@pytest.fixture
def sample_model():
    """Fixture for a sample ML model."""
    model = RandomForestClassifier(n_estimators=10, random_state=42)
    # Create dummy data to train
    import numpy as np
    X = np.random.rand(100, 5)
    y = np.random.randint(0, 2, 100)
    model.fit(X, y)
    return model


@pytest.fixture(autouse=True)
def cleanup_models():
    """Cleanup models directory before and after tests."""
    yield
    # Cleanup after test
    if settings.MODELS_PATH.exists():
        for item in settings.MODELS_PATH.iterdir():
            if item.is_dir():
                shutil.rmtree(item)


class TestFileOperation:
    """Test cases for File_Operation class."""

    def test_save_model_success(self, file_ops, sample_model):
        """Test successful model save."""
        result = file_ops.save_model(sample_model, "test_model")
        assert result == "success"

        # Verify file exists
        model_file = settings.MODELS_PATH / "test_model" / "test_model.joblib"
        assert model_file.exists()

    def test_save_model_overwrites_existing(self, file_ops, sample_model):
        """Test that saving overwrites existing model."""
        # Save first time
        file_ops.save_model(sample_model, "test_model")

        # Save again (should overwrite)
        result = file_ops.save_model(sample_model, "test_model")
        assert result == "success"

    def test_load_model_success(self, file_ops, sample_model):
        """Test successful model load."""
        # First save a model
        file_ops.save_model(sample_model, "test_model")

        # Then load it
        loaded_model = file_ops.load_model("test_model")
        assert loaded_model is not None
        assert hasattr(loaded_model, 'predict')

    def test_load_model_not_found(self, file_ops):
        """Test loading non-existent model raises error."""
        with pytest.raises(ModelPredictionError) as exc_info:
            file_ops.load_model("nonexistent_model")

        assert "Model file not found" in str(exc_info.value)

    def test_find_correct_model_file(self, file_ops, sample_model):
        """Test finding model by cluster number."""
        # Save models for different clusters
        file_ops.save_model(sample_model, "XGBoost_cluster_0")
        file_ops.save_model(sample_model, "XGBoost_cluster_1")

        # Find model for cluster 0
        model_name = file_ops.find_correct_model_file(0)
        assert "0" in model_name

        # Find model for cluster 1
        model_name = file_ops.find_correct_model_file(1)
        assert "1" in model_name

    def test_find_correct_model_file_not_found(self, file_ops):
        """Test finding non-existent cluster model raises error."""
        with pytest.raises(ModelPredictionError) as exc_info:
            file_ops.find_correct_model_file(99)

        assert "No model found for cluster" in str(exc_info.value)

    def test_delete_model_success(self, file_ops, sample_model):
        """Test successful model deletion."""
        # Save a model first
        file_ops.save_model(sample_model, "test_model")

        # Delete it
        result = file_ops.delete_model("test_model")
        assert result is True

        # Verify it's gone
        model_dir = settings.MODELS_PATH / "test_model"
        assert not model_dir.exists()

    def test_delete_model_not_exists(self, file_ops):
        """Test deleting non-existent model."""
        result = file_ops.delete_model("nonexistent")
        assert result is False

    def test_list_models_empty(self, file_ops):
        """Test listing models when none exist."""
        models = file_ops.list_models()
        assert models == []

    def test_list_models_with_models(self, file_ops, sample_model):
        """Test listing models when some exist."""
        # Save multiple models
        file_ops.save_model(sample_model, "model1")
        file_ops.save_model(sample_model, "model2")

        models = file_ops.list_models()
        assert len(models) == 2
        assert "model1" in models
        assert "model2" in models

    def test_backward_compatibility_pickle(self, file_ops, sample_model):
        """Test loading legacy pickle files and converting to joblib."""
        # Manually create a pickle file (simulating legacy format)
        import pickle
        model_dir = settings.MODELS_PATH / "legacy_model"
        model_dir.mkdir(parents=True, exist_ok=True)
        pickle_file = model_dir / "legacy_model.sav"

        with open(pickle_file, 'wb') as f:
            pickle.dump(sample_model, f)

        # Load using File_Operation (should convert to joblib)
        loaded_model = file_ops.load_model("legacy_model")
        assert loaded_model is not None

        # Verify joblib file now exists
        joblib_file = model_dir / "legacy_model.joblib"
        assert joblib_file.exists()
