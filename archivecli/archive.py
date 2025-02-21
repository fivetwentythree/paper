"""Core archive functionality for archivecli.

This module provides the main functionality for archiving URLs using archive.is service.
It integrates URL validation, archive service interaction, and browser handling.
"""

from typing import Optional, Tuple
from .validators import validate_url_with_reachability
from .archive_service import ArchiveService
from .browser_handler import open_url_in_browser
from .exceptions import (
    URLValidationError,
    URLReachabilityError,
    ArchiveServiceError,
    ArchiveNotFoundError,
    BrowserError
)
from .logging_config import get_logger

# Module-level logger
logger = get_logger(__name__)


def archive_url(url: str, quiet: bool = False) -> Tuple[bool, str]:
    """Archive a URL using archive.is and open it in the browser.
    
    This is the main function that coordinates the archiving process:
    1. Validates the URL format and reachability
    2. Checks for an existing archive or creates a new one
    3. Opens the archived version in the default browser
    
    Args:
        url: The URL to archive
        quiet: If True, suppress non-error output
        
    Returns:
        Tuple[bool, str]: A tuple containing:
            - bool: True if successful, False if failed
            - str: Success/error message
    
    Raises:
        URLValidationError: If the URL format is invalid
        URLReachabilityError: If the URL cannot be reached
        ArchiveServiceError: If there's an error with the archive service
        BrowserError: If there's an error opening the browser
    """
    try:
        # Validate URL format and reachability
        logger.info(f"Validating URL: {url}")
        validate_url_with_reachability(url)
        
        # Initialize archive service
        archive_service = ArchiveService()
        
        # Get archived version
        logger.info("Retrieving archived version...")
        archived_url = archive_service.get_latest_archive(url)
        
        # Open in browser
        logger.info(f"Opening archived URL: {archived_url}")
        success, message = open_url_in_browser(archived_url)
        
        if success:
            return True, f"Successfully opened archived version: {archived_url}"
        else:
            raise BrowserError(f"Failed to open browser: {message}")
            
    except (URLValidationError, URLReachabilityError) as e:
        logger.error(f"URL error: {str(e)}")
        return False, str(e)
    except ArchiveServiceError as e:
        logger.error(f"Archive service error: {str(e)}")
        return False, str(e)
    except BrowserError as e:
        logger.error(f"Browser error: {str(e)}")
        return False, str(e)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return False, f"An unexpected error occurred: {str(e)}"