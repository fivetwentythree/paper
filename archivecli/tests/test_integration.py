import pytest
from unittest.mock import patch, MagicMock
from archivecli.cli import main
from archivecli.validators import URLValidationError, URLReachabilityError
from archivecli.archive_service import ArchiveNotFoundError, ArchiveServiceError
from archivecli.browser_handler import BrowserError

@pytest.fixture
def mock_validate_url():
    with patch('archivecli.cli.validate_url_with_reachability') as mock:
        mock.return_value = 'https://example.com'
        yield mock

@pytest.fixture
def mock_archive_service():
    with patch('archivecli.cli.ArchiveService') as mock_class:
        mock_instance = MagicMock()
        mock_class.return_value = mock_instance
        mock_instance.get_latest_archive.return_value = 'https://archive.is/abc123'
        yield mock_instance

@pytest.fixture
def mock_browser():
    with patch('archivecli.cli.open_url_in_browser') as mock:
        mock.return_value = (True, 'Success')
        yield mock

def test_successful_workflow(mock_validate_url, mock_archive_service, mock_browser):
    """Test successful end-to-end workflow."""
    result = main(['https://example.com'])
    
    # Verify each step was called correctly
    mock_validate_url.assert_called_once_with('https://example.com')
    mock_archive_service.get_latest_archive.assert_called_once_with('https://example.com')
    mock_browser.assert_called_once_with('https://archive.is/abc123')
    
    # Verify successful exit code
    assert result == 0

def test_invalid_url(mock_validate_url, mock_archive_service, mock_browser):
    """Test behavior with invalid URL."""
    mock_validate_url.side_effect = URLValidationError('Invalid URL')
    
    result = main(['http://invalid'])
    
    mock_validate_url.assert_called_once_with('http://invalid')
    mock_archive_service.get_latest_archive.assert_not_called()
    mock_browser.assert_not_called()
    
    assert result == 2

def test_unreachable_url(mock_validate_url, mock_archive_service, mock_browser):
    """Test behavior with unreachable URL."""
    mock_validate_url.side_effect = URLReachabilityError('Connection failed')
    
    result = main(['https://unreachable.com'])
    
    mock_validate_url.assert_called_once_with('https://unreachable.com')
    mock_archive_service.get_latest_archive.assert_not_called()
    mock_browser.assert_not_called()
    
    assert result == 3

def test_no_archive_found(mock_validate_url, mock_archive_service, mock_browser):
    """Test behavior when no archive is found."""
    mock_archive_service.get_latest_archive.side_effect = ArchiveNotFoundError()
    
    result = main(['https://example.com'])
    
    mock_validate_url.assert_called_once_with('https://example.com')
    mock_archive_service.get_latest_archive.assert_called_once_with('https://example.com')
    mock_browser.assert_not_called()
    
    assert result == 4

def test_archive_service_error(mock_validate_url, mock_archive_service, mock_browser):
    """Test behavior when archive service fails."""
    mock_archive_service.get_latest_archive.side_effect = ArchiveServiceError('Service down')
    
    result = main(['https://example.com'])
    
    mock_validate_url.assert_called_once_with('https://example.com')
    mock_archive_service.get_latest_archive.assert_called_once_with('https://example.com')
    mock_browser.assert_not_called()
    
    assert result == 7

def test_browser_error(mock_validate_url, mock_archive_service, mock_browser):
    """Test behavior when browser fails to open."""
    mock_browser.side_effect = BrowserError('Failed to open browser')
    
    result = main(['https://example.com'])
    
    mock_validate_url.assert_called_once_with('https://example.com')
    mock_archive_service.get_latest_archive.assert_called_once_with('https://example.com')
    mock_browser.assert_called_once_with('https://archive.is/abc123')
    
    assert result == 8

def test_missing_url_argument():
    """Test behavior when no URL is provided."""
    result = main([])
    assert result != 0  # Should return non-zero exit code

def test_quiet_mode(mock_validate_url, mock_archive_service, mock_browser):
    """Test quiet mode operation."""
    result = main(['--quiet', 'https://example.com'])
    
    mock_validate_url.assert_called_once_with('https://example.com')
    mock_archive_service.get_latest_archive.assert_called_once_with('https://example.com')
    mock_browser.assert_called_once_with('https://archive.is/abc123')
    
    assert result == 0