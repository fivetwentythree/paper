"""Utilities to handle browser interactions for archivecli."""

from typing import Tuple
from urllib.parse import urlparse
import webbrowser

from .exceptions import BrowserError
from .logging_config import get_logger

logger = get_logger(__name__)


def validate_url(url: str) -> bool:
    """Return True if the given URL appears well formed."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def open_url_in_browser(url: str) -> Tuple[bool, str]:
    """Open the given URL in the system's default web browser."""
    if not validate_url(url):
        return False, "Invalid URL format"

    try:
        browser = webbrowser.get()
        if browser.open(url, new=2):
            return True, "URL opened successfully"
        return False, "Failed to open URL"
    except webbrowser.Error as exc:
        message = f"Browser error: {exc}"
        logger.error(message)
        raise BrowserError(message)
    except Exception as exc:
        message = f"Unexpected error opening URL: {exc}"
        logger.error(message)
        raise BrowserError(message)

