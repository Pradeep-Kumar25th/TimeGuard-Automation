"""
Logging Utility Functions
Enterprise-level logging configuration
"""

import logging
import os
from logging.handlers import RotatingFileHandler
from typing import Optional


def setup_logging(
    log_level: str = "INFO",
    log_file: Optional[str] = None,
    format_string: Optional[str] = None
) -> None:
    """
    Configure enterprise-level logging.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional log file path
        format_string: Optional custom format string
    """
    if format_string is None:
        format_string = (
            '%(asctime)s - %(name)s - %(levelname)s - '
            '%(message)s - [%(module)s:%(lineno)d]'
        )
    
    # Get log level
    level = getattr(logging, log_level.upper(), logging.INFO)
    
    # Configure root logger
    logging.root.setLevel(level)
    
    # Remove existing handlers
    logging.root.handlers = []
    
    # Console handler (for Azure App Service logs)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_formatter = logging.Formatter(format_string)
    console_handler.setFormatter(console_formatter)
    logging.root.addHandler(console_handler)
    
    # File handler (if specified)
    if log_file:
        try:
            # Ensure log directory exists
            log_dir = os.path.dirname(log_file)
            if log_dir:
                os.makedirs(log_dir, exist_ok=True)
            
            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=10 * 1024 * 1024,  # 10MB
                backupCount=5
            )
            file_handler.setLevel(level)
            file_formatter = logging.Formatter(format_string)
            file_handler.setFormatter(file_formatter)
            logging.root.addHandler(file_handler)
        except Exception as e:
            logging.warning(f"Could not set up file logging: {e}")


def get_logger(name: str) -> logging.Logger:
    """
    Get logger instance for a module.
    
    Args:
        name: Logger name (typically __name__)
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)

