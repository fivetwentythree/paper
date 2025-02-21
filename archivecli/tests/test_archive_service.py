import pytest
from unittest.mock import patch, Mock
from urllib.parse import urljoin, quote
from requests.exceptions import RequestException, Timeout

from archivecli.archive_service import (
    ArchiveService,
    ArchiveServiceError,
    ArchiveNotFoundError
)


@pytest.fixture
def archive_service():
    """Create an ArchiveService instance for testing."""
    return ArchiveService()


def test_construct_search_url(archive_service):
    """Test URL construction for archive.is searches."""
    url = "https://example.com"
    expected = f"https://archive.is/submit/?url={quote(url, safe='')}"
    assert archive_service.construct_search_url(url) == expected


def test_get_latest_archive_success(archive_service):
    """Test successful retrieval of an archived URL."""
    test_url = "https://example.com"
    archive_url = "https://archive.is/abc123"
    
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.url = archive_url
    
    with patch('requests.get', return_value=mock_response) as mock_get:
        result = archive_service.get_latest_archive(test_url)
        assert result == archive_url
        mock_get.assert_called_once()


def test_get_latest_archive_not_found(archive_service):
    """Test handling of URLs with no archived version."""
    test_url = "https://example.com"
    search_url = archive_service.construct_search_url(test_url)
    
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.url = search_url
    
    with patch('requests.get', return_value=mock_response):
        with pytest.raises(ArchiveNotFoundError, match="No archived version found"):
            archive_service.get_latest_archive(test_url)


@pytest.mark.parametrize("status_code,expected_error", [
    (404, ArchiveNotFoundError),
    (500, ArchiveServiceError),
    (503, ArchiveServiceError),
    (403, ArchiveServiceError),
])
def test_get_latest_archive_error_status(archive_service, status_code, expected_error):
    """Test handling of various HTTP error status codes."""
    mock_response = Mock()
    mock_response.status_code = status_code
    
    with patch('requests.get', return_value=mock_response):
        with pytest.raises(expected_error):
            archive_service.get_latest_archive("https://example.com")


def test_get_latest_archive_request_exception(archive_service):
    """Test handling of request exceptions."""
    with patch('requests.get', side_effect=RequestException("Connection error")):
        with pytest.raises(ArchiveServiceError, match="Failed to communicate"):
            archive_service.get_latest_archive("https://example.com")


def test_get_latest_archive_timeout(archive_service):
    """Test handling of request timeouts."""
    with patch('requests.get', side_effect=Timeout("Request timed out")):
        with pytest.raises(ArchiveServiceError, match="Failed to communicate"):
            archive_service.get_latest_archive("https://example.com")


def test_get_or_create_archive_existing(archive_service):
    """Test retrieving an existing archive."""
    test_url = "https://example.com"
    archive_url = "https://archive.is/abc123"
    
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.url = archive_url
    
    with patch('requests.get', return_value=mock_response):
        result = archive_service.get_or_create_archive(test_url)
        assert result == archive_url


def test_get_or_create_archive_not_implemented(archive_service):
    """Test that archive creation is not yet implemented."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.url = archive_service.construct_search_url("https://example.com")
    
    with patch('requests.get', return_value=mock_response):
        with pytest.raises(ArchiveServiceError, match="not yet implemented"):
            archive_service.get_or_create_archive("https://example.com")