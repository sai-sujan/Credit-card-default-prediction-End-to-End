"""
Enhanced logging module with proper log levels, rotation, and structured output.

This module provides industry-standard logging with:
- Multiple log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Automatic log rotation to prevent disk space issues
- Structured logging with timestamps and context
- Separate loggers for different modules
"""
import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional

from config import settings


class AppLogger:
    """
    Application logger with rotating file handler and console output.

    Features:
    - Automatic log file rotation (10MB max, 5 backups)
    - Configurable log levels
    - Console and file output
    - Structured log format with timestamps

    Example:
        logger = AppLogger.get_logger(__name__)
        logger.info("Processing started", extra={"records": 1000})
        logger.error("Failed to process", exc_info=True)
    """

    _loggers = {}

    @classmethod
    def get_logger(
        cls,
        name: str,
        log_file: Optional[Path] = None,
        level: Optional[str] = None
    ) -> logging.Logger:
        """
        Get or create a logger instance.

        Args:
            name: Logger name (usually __name__ of the calling module)
            log_file: Optional custom log file path
            level: Optional log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

        Returns:
            Configured logger instance
        """
        if name in cls._loggers:
            return cls._loggers[name]

        logger = logging.getLogger(name)
        log_level = getattr(logging, level or settings.LOG_LEVEL)
        logger.setLevel(log_level)

        # Prevent duplicate handlers
        if logger.handlers:
            return logger

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

        # File handler with rotation (if log_file provided)
        if log_file:
            log_file = Path(log_file)
            log_file.parent.mkdir(parents=True, exist_ok=True)

            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=10 * 1024 * 1024,  # 10MB
                backupCount=5,
                encoding='utf-8'
            )
            file_handler.setLevel(log_level)
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)

        cls._loggers[name] = logger
        return logger

    @classmethod
    def get_training_logger(cls, module_name: str) -> logging.Logger:
        """Get a logger for training operations."""
        log_file = settings.get_training_log_path(f"{module_name}.log")
        return cls.get_logger(f"training.{module_name}", log_file)

    @classmethod
    def get_prediction_logger(cls, module_name: str) -> logging.Logger:
        """Get a logger for prediction operations."""
        log_file = settings.get_prediction_log_path(f"{module_name}.log")
        return cls.get_logger(f"prediction.{module_name}", log_file)


# Backward compatibility: Keep old App_Logger class for existing code
class App_Logger:
    """
    Legacy logger class for backward compatibility.

    This class maintains the old interface while using the new logging system.
    New code should use AppLogger.get_logger() directly.
    """

    def __init__(self):
        """Initialize legacy logger."""
        self._logger: Optional[logging.Logger] = None

    def log(self, file_object, log_message: str) -> None:
        """
        Legacy log method that writes to file_object.

        Args:
            file_object: File object to write to (kept for compatibility but not used)
            log_message: Message to log
        """
        # Extract logger name from file object path if possible
        if hasattr(file_object, 'name'):
            file_path = Path(file_object.name)
            logger_name = file_path.stem

            # Determine if it's training or prediction based on path
            if 'Training' in str(file_path):
                self._logger = AppLogger.get_training_logger(logger_name)
            elif 'Prediction' in str(file_path):
                self._logger = AppLogger.get_prediction_logger(logger_name)
            else:
                self._logger = AppLogger.get_logger(logger_name, file_path)
        else:
            # Fallback to default logger
            if not self._logger:
                self._logger = AppLogger.get_logger('default')

        # Log at INFO level by default
        self._logger.info(log_message)


# Convenience functions
def get_logger(name: str) -> logging.Logger:
    """Convenience function to get a logger."""
    return AppLogger.get_logger(name)


def setup_logging(level: str = "INFO") -> None:
    """
    Setup application-wide logging configuration.

    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    logging.basicConfig(
        level=getattr(logging, level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
