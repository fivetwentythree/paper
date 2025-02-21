"""Module for handling browser-related operations.

This module provides functionality to open URLs in the user's default web browser
while handling various platform-specific issues and potential errors.
"""

import webbrowser
from typing import Tuple
import logging
from urllib.parse import urlparse


class BrowserError(Exception):
    """Exception raised for browser-related errors."""
    pass


def validate_url(url: str) -> bool:
    """Validate if the provided URL is properly formatted.
    
    Args:
        url: The URL to validate
        
    Returns:
        bool: True if URL is valid, False otherwise
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def open_url_in_browser(url: str) -> Tuple[bool, str]:
    """Open the provided URL in the system's default web browser.
    
    Args:
        url: The URL to open in the browser
        
    Returns:
        Tuple[bool, str]: A tuple containing:
            - bool: True if successful, False if failed
            - str: Success/error message
            
    Raises:
        BrowserError: If there's an error opening the browser
    """
    if not validate_url(url):
        return False, "Invalid URL format"
    
    try:
        # Attempt to open URL in a new browser window
        browser = webbrowser.get()
        if browser.open(url, new=2):
            return True, "URL opened successfully"
        else:
            return False, "Failed to open URL"
    except webbrowser.Error as e:
        error_msg = f"Browser error: {str(e)}"
        logging.error(error_msg)
        raise BrowserError(error_msg)
    except Exception as e:
        error_msg = f"Unexpected error opening URL: {str(e)}"
        logging.error(error_msg)
        raise BrowserError(error_msg)