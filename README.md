# Credit Card Default Prediction - End-to-End ML Pipeline

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A production-ready machine learning system for predicting credit card payment defaults with comprehensive data validation, preprocessing, model training, and prediction pipelines.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [API Documentation](#api-documentation)
- [Development](#development)
- [Testing](#testing)
- [Deployment](#deployment)
- [Project Structure](#project-structure)
- [Contributing](#contributing)

## 🎯 Overview

This project implements an end-to-end machine learning pipeline for predicting credit card payment defaults. The system includes:

- **Data Validation**: Schema-based validation with automated good/bad data segregation
- **Data Processing**: Automated preprocessing with imputation, scaling, and encoding
- **Model Training**: KMeans clustering with ensemble model training per cluster
- **Prediction API**: RESTful API for real-time predictions
- **MLOps**: Comprehensive logging, monitoring, and model versioning

### Problem Statement

Build a classification system to determine whether a person will default on their credit card payment next month based on historical payment behavior and demographics.

**Target Classes:**
- `1`: Customer will pay the bill (no default)
- `0`: Customer will not pay the bill (default)

## ✨ Features

### Production-Ready Code Quality
- ✅ **Type Hints**: Full type annotations throughout codebase
- ✅ **Error Handling**: Custom exceptions with detailed context
- ✅ **Logging**: Structured logging with rotation and levels
- ✅ **Testing**: 80%+ test coverage with pytest
- ✅ **Code Quality**: Pre-commit hooks with black, flake8, mypy
- ✅ **Configuration**: Centralized settings with environment variable support
- ✅ **Documentation**: Comprehensive docstrings and API docs

### ML Pipeline Features
- Automated data validation against schema
- Missing value imputation with SimpleImputer
- Feature scaling and categorical encoding
- Imbalanced dataset handling with RandomOverSampler
- KMeans clustering for data segmentation
- Hyperparameter tuning with GridSearchCV
- Model persistence with joblib
- Separate models per cluster for improved accuracy

## 🏗️ Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Raw Data  │────▶│  Validation  │────▶│  Database   │
└─────────────┘     └──────────────┘     └─────────────┘
                           │                     │
                           ▼                     ▼
                    ┌──────────────┐     ┌─────────────┐
                    │  Bad Data    │     │  Good Data  │
                    │  Archive     │     │  Processing │
                    └──────────────┘     └─────────────┘
                                                │
                                                ▼
                                        ┌───────────────┐
                                        │ Preprocessing │
                                        └───────────────┘
                                                │
                            ┌───────────────────┼───────────────────┐
                            ▼                   ▼                   ▼
                      ┌──────────┐       ┌──────────┐       ┌──────────┐
                      │ Cluster 0│       │ Cluster 1│       │ Cluster N│
                      │  Model   │       │  Model   │       │  Model   │
                      └──────────┘       └──────────┘       └──────────┘
                            │                   │                   │
                            └───────────────────┼───────────────────┘
                                                ▼
                                        ┌───────────────┐
                                        │  Predictions  │
                                        └───────────────┘
```

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/Credit-card-default-prediction-End-to-End.git
cd Credit-card-default-prediction-End-to-End
```

2. **Create and activate virtual environment**
```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

4. **Install pre-commit hooks** (for development)
```bash
pre-commit install
```

5. **Setup environment variables** (optional)
```bash
cp .env.example .env
# Edit .env with your settings
```

## 🚀 Quick Start

### Training the Model

```bash
# Start the Flask application
python main.py

# In another terminal, trigger training via API
curl -X POST http://localhost:5000/train
```

Or use the web interface at `http://localhost:5000/`

### Making Predictions

1. Place your CSV files in `Prediction_Batch_files/`
2. Ensure files match the schema in `schema_prediction.json`
3. Trigger prediction:

```bash
curl -X POST http://localhost:5000/predict
```

Results will be saved in `Prediction_Output_File/Predictions.csv`

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# Server
HOST=0.0.0.0
PORT=5000
DEBUG=False

# Paths
TRAINING_BATCH_PATH=Training_Batch_Files
MODELS_PATH=models

# ML Configuration
RANDOM_STATE=42
TEST_SIZE=0.33

# Logging
LOG_LEVEL=INFO
```

### Configuration Management

All settings are centralized in `config/settings.py`. The configuration system:
- Supports environment variables
- Provides sensible defaults
- Automatically creates required directories
- Uses `pathlib.Path` for cross-platform compatibility

```python
from config import settings

# Access configuration
model_path = settings.MODELS_PATH
log_level = settings.LOG_LEVEL
```

## 📚 API Documentation

### Endpoints

#### `GET /`
Returns the web interface for training and prediction.

#### `POST /train`
Triggers the model training pipeline.

**Response:**
```json
{
  "status": "success",
  "message": "Training completed successfully"
}
```

#### `POST /predict`
Triggers the prediction pipeline.

**Response:**
```json
{
  "status": "success",
  "predictions_file": "Prediction_Output_File/Predictions.csv"
}
```

## 🛠️ Development

### Code Style

This project follows strict code quality standards:

```bash
# Format code with black
black . --line-length=100

# Sort imports
isort .

# Lint code
flake8 .

# Type check
mypy .

# Run all checks
pre-commit run --all-files
```

### Project Structure

```
Credit-card-default-prediction-End-to-End/
│
├── config/                          # Configuration management
│   ├── __init__.py
│   └── settings.py                  # Centralized settings
│
├── utils/                           # Utility modules
│   ├── __init__.py
│   └── exceptions.py                # Custom exceptions
│
├── application_logging/             # Logging module
│   └── logger.py                    # Enhanced logger
│
├── data_preprocessing/              # Data preprocessing
│   └── preprocessing.py             # Preprocessor class
│
├── file_operations/                 # Model persistence
│   └── file_methods.py              # File operations with joblib
│
├── best_model_finder/               # Model selection
│   └── tuner.py                     # Hyperparameter tuning
│
├── data_ingestion/                  # Data loading
│   ├── data_loader.py
│   └── data_loader_prediction.py
│
├── Training_Raw_Data_Validation/    # Training validation
│   └── rawValidation.py
│
├── Prediction_Raw_Data_Validation/  # Prediction validation
│   └── predictionDataValidation.py
│
├── tests/                           # Test suite
│   ├── test_config.py
│   ├── test_exceptions.py
│   ├── test_file_operations.py
│   ├── test_preprocessing.py
│   └── test_api.py
│
├── main.py                          # Flask application
├── trainingModel.py                 # Training pipeline
├── predictFromModel.py              # Prediction pipeline
├── requirements.txt                 # Dependencies
├── pyproject.toml                   # Tool configuration
├── .pre-commit-config.yaml          # Pre-commit hooks
├── .env.example                     # Environment template
└── README.md                        # This file
```

## 🧪 Testing

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_preprocessing.py

# Run with verbose output
pytest -v
```

### Test Coverage

Target: **80%+ coverage**

```bash
# Generate coverage report
pytest --cov=. --cov-report=term-missing

# View HTML coverage report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

## 🚀 Deployment

### Docker

```bash
# Build image
docker build -t credit-card-default-prediction .

# Run container
docker run -p 5000:5000 credit-card-default-prediction
```

### Heroku

```bash
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Deploy
git push heroku main
```

### CircleCI

The project includes CircleCI configuration for:
- Automated testing on every commit
- Docker image building
- Deployment to Heroku

Required environment variables in CircleCI:
- `DOCKERHUB_USER`
- `DOCKER_HUB_PASSWORD_USER`
- `HEROKU_API_KEY`
- `HEROKU_APP_NAME`
- `HEROKU_EMAIL_ADDRESS`

## 📊 Model Performance

The system uses:
- **Clustering**: KMeans with elbow method (1-10 clusters)
- **Classification**: XGBoost and Naive Bayes per cluster
- **Evaluation**: AUC-ROC and Accuracy metrics
- **Data Balancing**: RandomOverSampler for imbalanced classes

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and code quality checks (`pre-commit run --all-files`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Dataset source: UCI Machine Learning Repository
- Built with scikit-learn, XGBoost, and Flask
- Inspired by modern MLOps practices

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Built with ❤️ using industry best practices**
