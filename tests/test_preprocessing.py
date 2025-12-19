"""Tests for data preprocessing module."""
import pytest
import pandas as pd
import numpy as np
from application_logging.logger import App_Logger
from data_preprocessing.preprocessing import Preprocessor


@pytest.fixture
def sample_data():
    """Create sample DataFrame for testing."""
    return pd.DataFrame({
        'id': [1, 2, 3, 4, 5],
        'feature1': [10, 20, 30, 40, 50],
        'feature2': [1.5, 2.5, 3.5, 4.5, 5.5],
        'category': ['A', 'B', 'A', 'C', 'B'],
        'target': [0, 1, 0, 1, 0]
    })


@pytest.fixture
def data_with_nulls():
    """Create DataFrame with missing values."""
    return pd.DataFrame({
        'feature1': [10, None, 30, 40, None],
        'feature2': [1.5, 2.5, None, 4.5, 5.5],
        'category': ['A', None, 'A', 'C', 'B'],
        'target': [0, 1, 0, 1, 0]
    })


@pytest.fixture
def data_with_spaces():
    """Create DataFrame with unwanted spaces."""
    return pd.DataFrame({
        'category': ['  A  ', ' B ', 'C  ', '  D', 'E'],
        'name': ['John  ', '  Jane', ' Bob ', 'Alice', '  Charlie  ']
    })


@pytest.fixture
def preprocessor():
    """Create Preprocessor instance with dummy logger."""
    class DummyFile:
        def write(self, msg):
            pass

    file_obj = DummyFile()
    logger = App_Logger()
    return Preprocessor(file_obj, logger)


class TestPreprocessor:
    """Test cases for Preprocessor class."""

    def test_remove_unwanted_spaces(self, preprocessor, data_with_spaces):
        """Test removing unwanted spaces from string columns."""
        result = preprocessor.remove_unwanted_spaces(data_with_spaces)

        assert result['category'].tolist() == ['A', 'B', 'C', 'D', 'E']
        assert result['name'].tolist() == ['John', 'Jane', 'Bob', 'Alice', 'Charlie']

    def test_remove_columns(self, preprocessor, sample_data):
        """Test removing specified columns."""
        columns_to_remove = ['id', 'target']
        result = preprocessor.remove_columns(sample_data, columns_to_remove)

        assert 'id' not in result.columns
        assert 'target' not in result.columns
        assert 'feature1' in result.columns
        assert 'feature2' in result.columns

    def test_separate_label_feature(self, preprocessor, sample_data):
        """Test separating features and labels."""
        X, y = preprocessor.separate_label_feature(sample_data, 'target')

        assert 'target' not in X.columns
        assert 'feature1' in X.columns
        assert len(y) == len(sample_data)
        assert y.name == 'target'

    def test_is_null_present_with_nulls(self, preprocessor, data_with_nulls):
        """Test detecting null values."""
        null_present, cols_with_nulls = preprocessor.is_null_present(data_with_nulls)

        assert null_present is True
        assert 'feature1' in cols_with_nulls
        assert 'feature2' in cols_with_nulls
        assert 'category' in cols_with_nulls

    def test_is_null_present_without_nulls(self, preprocessor, sample_data):
        """Test detecting no null values."""
        null_present, cols_with_nulls = preprocessor.is_null_present(sample_data)

        assert null_present is False
        assert len(cols_with_nulls) == 0

    def test_impute_missing_values(self, preprocessor, data_with_nulls):
        """Test imputing missing values."""
        cols_with_nulls = ['feature1', 'feature2', 'category']
        result = preprocessor.impute_missing_values(data_with_nulls, cols_with_nulls)

        # Check no nulls remain in specified columns
        assert result['feature1'].isna().sum() == 0
        assert result['feature2'].isna().sum() == 0
        assert result['category'].isna().sum() == 0

    def test_scale_numerical_columns(self, preprocessor, sample_data):
        """Test scaling numerical columns."""
        result = preprocessor.scale_numerical_columns(sample_data)

        # Check that result has numerical columns scaled
        assert len(result) == len(sample_data)
        # Scaled values should have mean close to 0 and std close to 1
        assert abs(result['feature1'].mean()) < 1e-10
        assert abs(result['feature1'].std() - 1.0) < 1e-10

    def test_encode_categorical_columns(self, preprocessor, sample_data):
        """Test encoding categorical columns."""
        result = preprocessor.encode_categorical_columns(sample_data)

        # Original categorical column should be gone, dummy columns created
        assert 'category' not in result.columns
        # Should have dummy columns (with drop_first=True)
        assert any('category_' in col for col in result.columns)

    def test_handle_imbalanced_dataset(self, preprocessor):
        """Test handling imbalanced dataset with RandomOverSampler."""
        # Create imbalanced dataset
        X = pd.DataFrame({
            'feature1': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            'feature2': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        })
        y = pd.Series([0, 0, 0, 0, 0, 0, 0, 0, 1, 1])  # 80% class 0, 20% class 1

        X_balanced, y_balanced = preprocessor.handle_imbalanced_dataset(X, y)

        # After balancing, classes should be equal
        unique, counts = np.unique(y_balanced, return_counts=True)
        assert counts[0] == counts[1]  # Equal class distribution
