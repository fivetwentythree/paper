"""Centralized logging configuration for archivecli.

This module provides a consistent logging configuration across all archivecli modules.
It sets up logging levels, formatters, and handlers based on the application's needs.
"""

import logging
from typing import Optional

# Default format for log messages
DEFAULT_LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
DEFAULT_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

# Module-level logger
logger = logging.getLogger(__name__)

def configure_logging(quiet: bool = False, log_level: Optional[int] = None) -> None:
    """Configure logging for the entire application.
    
    Args:
        quiet: If True, suppress all non-error output
        log_level: Optional logging level to override default (logging.INFO)
    """
    # Set up the root logger
    root_logger = logging.getLogger('archivecli')
    
    # Clear any existing handlers
    root_logger.handlers.clear()
    
    # Set the base logging level
    if log_level is not None:
        root_logger.setLevel(log_level)
    else:
        root_logger.setLevel(logging.DEBUG if not quiet else logging.ERROR)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.ERROR if quiet else logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter(
        fmt=DEFAULT_LOG_FORMAT,
        datefmt=DEFAULT_DATE_FORMAT
    )
    console_handler.setFormatter(formatter)
    
    # Add handler to root logger
    root_logger.addHandler(console_handler)
    
    logger.debug('Logging configured: quiet=%s, level=%s', 
                quiet, 
                logging.getLevelName(root_logger.level))

def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for a module.
    
    Args:
        name: Name of the module requesting the logger
        
    Returns:
        logging.Logger: Configured logger instance
    """
    return logging.getLogger(f'archivecli.{name}')