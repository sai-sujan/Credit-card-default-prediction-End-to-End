"""
Model file operations with joblib serialization and proper error handling.

This module handles all model persistence operations including:
- Saving trained models
- Loading models for prediction
- Finding models by cluster number
- Model versioning support
"""
import joblib
import os
import shutil
from pathlib import Path
from typing import Any, Optional
import logging

from config import settings
from utils.exceptions import FileOperationError, ModelPredictionError


class File_Operation:
    """
    Handles model file operations with industry-standard practices.

    Features:
    - joblib serialization (faster and safer than pickle for ML models)
    - Proper error handling with custom exceptions
    - Type hints for better code clarity
    - Context managers for safe file operations
    - Logging for all operations
    """

    def __init__(self, file_object=None, logger_object=None):
        """
        Initialize file operations handler.

        Args:
            file_object: Legacy parameter, kept for backward compatibility
            logger_object: Legacy parameter, kept for backward compatibility
        """
        self.logger = logging.getLogger(__name__)
        self.model_directory = settings.MODELS_PATH

        # Ensure model directory exists
        self.model_directory.mkdir(parents=True, exist_ok=True)

    def save_model(self, model: Any, filename: str) -> str:
        """
        Save a machine learning model to disk using joblib.

        Args:
            model: The trained model object to save
            filename: Name for the model file (without extension)

        Returns:
            'success' if save operation completed successfully

        Raises:
            FileOperationError: If model save fails
        """
        self.logger.info(f"Saving model: {filename}")

        try:
            model_path = self.model_directory / filename

            # Create directory for this model
            if model_path.is_dir():
                self.logger.warning(f"Removing existing model directory: {filename}")
                shutil.rmtree(model_path)

            model_path.mkdir(parents=True, exist_ok=True)

            # Save model with joblib (more efficient than pickle for large numpy arrays)
            model_file = model_path / f"{filename}.joblib"
            joblib.dump(model, model_file, compress=3)

            self.logger.info(f"Model '{filename}' saved successfully at {model_file}")
            return 'success'

        except Exception as e:
            error_msg = f"Failed to save model '{filename}'"
            self.logger.error(error_msg, exc_info=True)
            raise FileOperationError(
                error_msg,
                details={'filename': filename, 'error': str(e)}
            ) from e

    def load_model(self, filename: str) -> Any:
        """
        Load a machine learning model from disk.

        Args:
            filename: Name of the model file (without extension)

        Returns:
            The loaded model object

        Raises:
            ModelPredictionError: If model file doesn't exist
            FileOperationError: If model load fails
        """
        self.logger.info(f"Loading model: {filename}")

        try:
            model_file = self.model_directory / filename / f"{filename}.joblib"

            if not model_file.exists():
                # Try legacy pickle format for backward compatibility
                legacy_file = self.model_directory / filename / f"{filename}.sav"
                if legacy_file.exists():
                    self.logger.warning(f"Loading legacy pickle file: {legacy_file}")
                    import pickle
                    with open(legacy_file, 'rb') as f:
                        model = pickle.load(f)
                    # Re-save in joblib format
                    self.save_model(model, filename)
                    return model
                else:
                    raise ModelPredictionError(
                        f"Model file not found: {filename}",
                        details={'expected_path': str(model_file)}
                    )

            model = joblib.load(model_file)
            self.logger.info(f"Model '{filename}' loaded successfully")
            return model

        except ModelPredictionError:
            raise
        except Exception as e:
            error_msg = f"Failed to load model '{filename}'"
            self.logger.error(error_msg, exc_info=True)
            raise FileOperationError(
                error_msg,
                details={'filename': filename, 'error': str(e)}
            ) from e

    def find_correct_model_file(self, cluster_number: int) -> str:
        """
        Find the model file corresponding to a cluster number.

        Args:
            cluster_number: The cluster number to find the model for

        Returns:
            The model filename (without extension)

        Raises:
            ModelPredictionError: If no model found for the cluster
        """
        self.logger.info(f"Finding model for cluster: {cluster_number}")

        try:
            cluster_str = str(cluster_number)
            list_of_files = os.listdir(self.model_directory)

            model_name = None
            for file in list_of_files:
                if cluster_str in file:
                    model_name = file
                    break

            if model_name is None:
                raise ModelPredictionError(
                    f"No model found for cluster {cluster_number}",
                    details={
                        'cluster': cluster_number,
                        'available_models': list_of_files
                    }
                )

            # Remove file extension if present
            model_name = model_name.split('.')[0]

            self.logger.info(f"Found model '{model_name}' for cluster {cluster_number}")
            return model_name

        except ModelPredictionError:
            raise
        except Exception as e:
            error_msg = f"Error finding model for cluster {cluster_number}"
            self.logger.error(error_msg, exc_info=True)
            raise FileOperationError(
                error_msg,
                details={'cluster': cluster_number, 'error': str(e)}
            ) from e

    def delete_model(self, filename: str) -> bool:
        """
        Delete a model file and its directory.

        Args:
            filename: Name of the model to delete

        Returns:
            True if deletion was successful

        Raises:
            FileOperationError: If deletion fails
        """
        self.logger.info(f"Deleting model: {filename}")

        try:
            model_path = self.model_directory / filename

            if model_path.exists():
                shutil.rmtree(model_path)
                self.logger.info(f"Model '{filename}' deleted successfully")
                return True
            else:
                self.logger.warning(f"Model '{filename}' does not exist")
                return False

        except Exception as e:
            error_msg = f"Failed to delete model '{filename}'"
            self.logger.error(error_msg, exc_info=True)
            raise FileOperationError(
                error_msg,
                details={'filename': filename, 'error': str(e)}
            ) from e

    def list_models(self) -> list:
        """
        List all available models.

        Returns:
            List of model names
        """
        try:
            if not self.model_directory.exists():
                return []

            models = [f.name for f in self.model_directory.iterdir() if f.is_dir()]
            self.logger.info(f"Found {len(models)} models")
            return models

        except Exception as e:
            self.logger.error("Failed to list models", exc_info=True)
            raise FileOperationError(
                "Failed to list models",
                details={'error': str(e)}
            ) from e
