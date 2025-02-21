import pytest
import requests
from unittest.mock import patch
from requests.exceptions import RequestException, Timeout, TooManyRedirects, SSLError

from archivecli.validators import (
    check_url_reachability,
    validate_url_with_reachability,
    URLReachabilityError
)

# ... (keep existing validation tests) ...

@pytest.fixture
def mock_response():
    """Create a mock response object."""
    class MockResponse:
        def __init__(self, status_code=200, url=None):
            self.status_code = status_code
            self.url = url or "https://example.com"
    return MockResponse


def test_successful_reachability(mock_response):
    """Test successful URL reachability check."""
    with patch('requests.head') as mock_head:
        mock_head.return_value = mock_response()
        url, reachable = check_url_reachability("https://example.com")
        assert reachable
        assert url == "https://example.com"


def test_redirect_handling(mock_response):
    """Test handling of redirected URLs."""
    with patch('requests.head') as mock_head:
        final_url = "https://example.com/final"
        mock_head.return_value = mock_response(url=final_url)
        url, reachable = check_url_reachability("https://example.com")
        assert reachable
        assert url == final_url


@pytest.mark.parametrize("status_code,expected_error", [
    (403, "Access forbidden"),
    (404, "Page not found"),
    (500, "Server error occurred"),
    (502, "Server error occurred"),
])
def test_error_status_codes(mock_response, status_code, expected_error):
    """Test handling of various HTTP error status codes."""
    with patch('requests.head') as mock_head:
        mock_head.return_value = mock_response(status_code=status_code)
        with pytest.raises(URLReachabilityError, match=expected_error):
            check_url_reachability("https://example.com")


@pytest.mark.parametrize("exception,expected_error", [
    (Timeout, "Request timed out"),
    (TooManyRedirects, "Too many redirects"),
    (SSLError, "SSL verification failed"),
    (RequestException("Custom error"), "Request failed: Custom error"),
])
def test_request_exceptions(exception, expected_error):
    """Test handling of various request exceptions."""
    with patch('requests.head') as mock_head:
        mock_head.side_effect = exception
        with pytest.raises(URLReachabilityError, match=expected_error):
            check_url_reachability("https://example.com")


def test_validate_url_with_reachability_success():
    """Test successful complete URL validation with reachability."""
    with patch('requests.head') as mock_head:
        mock_head.return_value = mock_response()
        result = validate_url_with_reachability("https://example.com")
        assert result == "https://example.com"


def test_validate_url_with_reachability_timeout():
    """Test timeout handling in complete validation."""
    with patch('requests.head') as mock_head:
        mock_head.side_effect = Timeout
        with pytest.raises(URLReachabilityError, match="Request timed out"):
            validate_url_with_reachability("https://example.com", timeout=5)