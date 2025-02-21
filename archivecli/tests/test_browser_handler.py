import pytest
from unittest.mock import patch, Mock
from webbrowser import Error as WebBrowserError

from archivecli.browser_handler import (
    validate_url,
    open_url_in_browser,
    BrowserError
)


def test_validate_url_valid():
    """Test URL validation with valid URLs."""
    valid_urls = [
        "https://example.com",
        "http://test.org/path?param=value",
        "ftp://files.example.com"
    ]
    for url in valid_urls:
        assert validate_url(url)


def test_validate_url_invalid():
    """Test URL validation with invalid URLs."""
    invalid_urls = [
        "",  # Empty string
        "not_a_url",  # No scheme or domain
        "http://",  # No domain
        "://example.com",  # No scheme
        "http:example.com"  # Malformed URL
    ]
    for url in invalid_urls:
        assert not validate_url(url)


def test_open_url_success():
    """Test successful URL opening in browser."""
    test_url = "https://example.com"
    
    mock_browser = Mock()
    mock_browser.open.return_value = True
    
    with patch('webbrowser.get', return_value=mock_browser):
        success, message = open_url_in_browser(test_url)
        assert success
        assert message == "URL opened successfully"
        mock_browser.open.assert_called_once_with(test_url, new=2)


def test_open_url_browser_failure():
    """Test handling of browser failure when opening URL."""
    test_url = "https://example.com"
    
    mock_browser = Mock()
    mock_browser.open.return_value = False
    
    with patch('webbrowser.get', return_value=mock_browser):
        success, message = open_url_in_browser(test_url)
        assert not success
        assert message == "Failed to open URL"


def test_open_url_invalid_url():
    """Test opening invalid URL."""
    invalid_url = "not_a_valid_url"
    success, message = open_url_in_browser(invalid_url)
    assert not success
    assert message == "Invalid URL format"


def test_open_url_browser_error():
    """Test handling of browser errors."""
    test_url = "https://example.com"
    error_message = "Browser not found"
    
    with patch('webbrowser.get', side_effect=WebBrowserError(error_message)):
        with pytest.raises(BrowserError, match=f"Browser error: {error_message}"):
            open_url_in_browser(test_url)


def test_open_url_unexpected_error():
    """Test handling of unexpected errors."""
    test_url = "https://example.com"
    error_message = "Unexpected error"
    
    with patch('webbrowser.get', side_effect=Exception(error_message)):
        with pytest.raises(BrowserError, match=f"Unexpected error opening URL: {error_message}"):
            open_url_in_browser(test_url)