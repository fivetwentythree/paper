from typing import Optional
import requests
import logging
from urllib.parse import urljoin, quote
from requests.exceptions import RequestException
from .logging_config import get_logger
from .exceptions import (
    ArchiveServiceError,
    ArchiveNotFoundError,
    ArchiveServiceUnavailableError,
    ArchiveCreationError
)

# Module-level logger
logger = get_logger(__name__)


class ArchiveService:
    """Service class for interacting with archive.is."""
    
    BASE_URL = "https://archive.is/"
    SUBMIT_ENDPOINT = "submit/"
    
    def __init__(self):
        # Browser-like headers to avoid blocks
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        }
    
    def construct_search_url(self, url: str) -> str:
        """Construct the archive.is search URL for a given URL.
        
        Args:
            url: The URL to search for in archive.is
            
        Returns:
            str: The complete archive.is search URL
        """
        # URL encode the target URL and construct the search URL
        encoded_url = quote(url, safe='')
        return urljoin(self.BASE_URL, f"{self.SUBMIT_ENDPOINT}?url={encoded_url}")
    
    def get_latest_archive(self, url: str, timeout: int = 10) -> str:
        """Get the most recent archived version of a URL from archive.is.
        
        Args:
            url: The URL to find archives for
            timeout: Request timeout in seconds
            
        Returns:
            str: URL of the most recent archive
            
        Raises:
            ArchiveServiceError: If there's an error communicating with archive.is
            ArchiveNotFoundError: If no archive is found for the URL
        """
        try:
            search_url = self.construct_search_url(url)
            logger.debug(f"Constructed search URL: {search_url}")
            
            response = requests.get(
                search_url,
                headers=self.headers,
                timeout=timeout,
                allow_redirects=True
            )
            logger.debug(f"Received response with status code: {response.status_code}")
            
            # Check for various response scenarios
            if response.status_code == 200:
                # If redirected to an archive page, that's the latest archive
                if 'archive.is/' in response.url and response.url != search_url:
                    logger.debug(f"Found archive at: {response.url}")
                    return response.url
                
                # TODO: Implement HTML parsing to extract archive URL if not redirected
                # This would handle cases where multiple archives are available
                logger.warning("No archive found in response content")
                raise ArchiveNotFoundError("No archived version found")
                
            elif response.status_code == 404:
                logger.warning(f"No archive found for URL: {url}")
                raise ArchiveNotFoundError("No archived version found")
            elif response.status_code >= 500:
                logger.error("Archive.is service returned server error")
                raise ArchiveServiceUnavailableError(
                    "Archive.is service is temporarily unavailable. Please try again later."
                )
            else:
                logger.error(f"Unexpected response status: {response.status_code}")
                raise ArchiveServiceError(
                    f"Received unexpected response from archive.is (status code: {response.status_code}). "
                    "Please try again or report this issue if it persists."
                )
                
        except RequestException as e:
            raise ArchiveServiceError(f"Failed to communicate with archive.is: {str(e)}")
    
    def get_or_create_archive(self, url: str, timeout: int = 10) -> str:
        """Get the latest archive of a URL or create a new one if none exists.
        
        Args:
            url: The URL to archive
            timeout: Request timeout in seconds
            
        Returns:
            str: URL of the archive (either existing or newly created)
            
        Raises:
            ArchiveServiceError: If there's an error communicating with archive.is
        """
        try:
            return self.get_latest_archive(url, timeout)
        except ArchiveNotFoundError:
            logger.info(f"No existing archive found for {url}, attempting to create new archive...")
            raise ArchiveCreationError(
                "Archive creation is not yet implemented. "
                "Please try again later when this feature becomes available."
            )