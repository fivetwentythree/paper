import pytest
import json
import tempfile
from pathlib import Path

from archivecli.domain_blocker import DomainBlocker, DomainBlockerError


@pytest.fixture
def domain_blocker():
    """Create a DomainBlocker instance for testing."""
    return DomainBlocker()


@pytest.fixture
def temp_config_file():
    """Create a temporary configuration file for testing."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump({'blocked_domains': ['test.com', 'example.org']}, f)
        return Path(f.name)


def test_default_blocked_domains(domain_blocker):
    """Test that default blocked domains are loaded."""
    blocked_domains = domain_blocker.get_blocked_domains()
    assert 'facebook.com' in blocked_domains
    assert 'twitter.com' in blocked_domains


def test_load_config(temp_config_file):
    """Test loading blocked domains from configuration file."""
    blocker = DomainBlocker(str(temp_config_file))
    blocked_domains = blocker.get_blocked_domains()
    assert 'test.com' in blocked_domains
    assert 'example.org' in blocked_domains


def test_load_config_invalid_file():
    """Test loading configuration from invalid file."""
    with pytest.raises(DomainBlockerError, match="Failed to load configuration"):
        DomainBlocker("nonexistent.json")


def test_is_domain_blocked(domain_blocker):
    """Test checking if domains are blocked."""
    assert domain_blocker.is_domain_blocked("https://www.facebook.com/path")
    assert domain_blocker.is_domain_blocked("http://twitter.com")
    assert not domain_blocker.is_domain_blocked("https://example.com")


def test_is_domain_blocked_with_www(domain_blocker):
    """Test that www prefix is handled correctly."""
    assert domain_blocker.is_domain_blocked("https://www.facebook.com")
    assert domain_blocker.is_domain_blocked("https://facebook.com")


def test_add_blocked_domain(domain_blocker):
    """Test adding new blocked domains."""
    domain_blocker.add_blocked_domain("example.com")
    assert domain_blocker.is_domain_blocked("https://example.com")
    assert "example.com" in domain_blocker.get_blocked_domains()


def test_remove_blocked_domain(domain_blocker):
    """Test removing blocked domains."""
    domain = "facebook.com"
    domain_blocker.remove_blocked_domain(domain)
    assert not domain_blocker.is_domain_blocked(f"https://{domain}")
    assert domain not in domain_blocker.get_blocked_domains()


def test_remove_nonexistent_domain(domain_blocker):
    """Test removing a domain that isn't blocked."""
    with pytest.raises(DomainBlockerError, match="not in the blocked list"):
        domain_blocker.remove_blocked_domain("nonexistent.com")


def test_save_config(domain_blocker, tmp_path):
    """Test saving configuration to file."""
    config_path = tmp_path / "config.json"
    domain_blocker.save_config(str(config_path))
    
    # Verify file contents
    with open(config_path) as f:
        config = json.load(f)
        assert 'blocked_domains' in config
        assert isinstance(config['blocked_domains'], list)
        assert set(config['blocked_domains']) == domain_blocker.get_blocked_domains()


def test_case_insensitive_domains(domain_blocker):
    """Test that domain matching is case-insensitive."""
    domain_blocker.add_blocked_domain("Example.com")
    assert domain_blocker.is_domain_blocked("https://example.com")
    assert domain_blocker.is_domain_blocked("https://EXAMPLE.COM")


def test_invalid_url_format(domain_blocker):
    """Test handling of invalid URL formats."""
    with pytest.raises(DomainBlockerError, match="Failed to parse URL"):
        domain_blocker.is_domain_blocked("not-a-valid-url")