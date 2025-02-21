from urllib.parse import urlparse
from typing import Optional, Tuple
import requests
from requests.exceptions import RequestException
from .domain_blocker import DomainBlocker, DomainBlockerError


class URLValidationError(Exception):
    """Custom exception for URL validation errors."""
    pass


class URLReachabilityError(Exception):
    """Custom exception for URL reachability errors."""
    pass


def is_valid_scheme(url: str) -> bool:
    """
    Check if the URL starts with http:// or https://.
    
    Args:
        url: The URL to validate
        
    Returns:
        bool: True if the URL has a valid scheme, False otherwise
    """
    try:
        parsed = urlparse(url)
        return parsed.scheme in ('http', 'https')
    except Exception:
        return False


def is_well_formed_url(url: str) -> bool:
    """
    Check if a URL is well-formed using urllib.parse.
    
    Args:
        url: The URL to validate
        
    Returns:
        bool: True if the URL is well-formed, False otherwise
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def check_url_reachability(url: str, timeout: int = 10) -> Tuple[str, bool]:
    """
    Check if a URL is reachable and follow redirects if necessary.
    
    Args:
        url: The URL to check
        timeout: Timeout in seconds for the request
        
    Returns:
        Tuple[str, bool]: (Final URL after redirects, True if reachable)
        
    Raises:
        URLReachabilityError: If the URL is unreachable or encounters an error
    """
    try:
        response = requests.head(
            url,
            allow_redirects=True,
            timeout=timeout,
            headers={'User-Agent': 'archivecli/1.0'}
        )
        
        # Check if we got redirected
        final_url = response.url
        
        # Handle common status codes
        if response.status_code == 200:
            return final_url, True
        elif response.status_code == 403:
            raise URLReachabilityError("Access forbidden")
        elif response.status_code == 404:
            raise URLReachabilityError("Page not found")
        elif response.status_code >= 500:
            raise URLReachabilityError("Server error occurred")
        else:
            raise URLReachabilityError(f"Unexpected status code: {response.status_code}")
            
    except requests.exceptions.Timeout:
        raise URLReachabilityError("Request timed out")
    except requests.exceptions.TooManyRedirects:
        raise URLReachabilityError("Too many redirects")
    except requests.exceptions.SSLError:
        raise URLReachabilityError("SSL verification failed")
    except RequestException as e:
        raise URLReachabilityError(f"Request failed: {str(e)}")


def validate_url_with_reachability(url: str, timeout: int = 10, domain_blocker: Optional[DomainBlocker] = None) -> str:
    """Perform complete URL validation including reachability check and domain blocking.
    
    Args:
        url: The URL to validate
        timeout: Timeout in seconds for the request
        domain_blocker: Optional DomainBlocker instance to check for blocked domains
        
    Returns:
        str: The final URL after following any redirects
        
    Raises:
        URLValidationError: If the URL is invalid
        URLReachabilityError: If the URL is unreachable
        DomainBlockerError: If the domain is blocked or there's an error checking the domain
    """
    if not is_well_formed_url(url):
        raise URLValidationError("Invalid URL format")
        
    if not is_valid_scheme(url):
        raise URLValidationError("URL must start with http:// or https://")
    
    if domain_blocker and domain_blocker.is_domain_blocked(url):
        raise URLValidationError("Domain is blocked")
        
    final_url, reachable = check_url_reachability(url, timeout)
    return final_url


def validate_url(url: str) -> Optional[str]:
    """
    Validate a URL, checking both scheme and format.
    
    Args:
        url: The URL to validate
        
    Returns:
        str: The validated URL
        
    Raises:
        URLValidationError: If the URL is invalid
    """
    if not url:
        raise URLValidationError("URL cannot be empty")
    
    if not is_valid_scheme(url):
        raise URLValidationError("URL must start with http:// or https://")
    
    if not is_well_formed_url(url):
        raise URLValidationError("URL is not well-formed")
    
    return url