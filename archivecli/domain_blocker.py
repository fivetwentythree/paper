"""Module for managing blocked domains in archivecli."""
from typing import Set, Optional
from urllib.parse import urlparse
import json
import os
from pathlib import Path


class DomainBlockerError(Exception):
    """Custom exception for domain blocker errors."""
    pass


class DomainBlocker:
    """Manages blocked domains for archivecli."""

    # Default blocked domains
    DEFAULT_BLOCKED_DOMAINS = {
        'facebook.com',
        'twitter.com',
        'instagram.com',
        'linkedin.com',
        'accounts.google.com',
        'login.yahoo.com',
    }

    def __init__(self, config_path: Optional[str] = None):
        """Initialize the domain blocker.

        Args:
            config_path: Optional path to a JSON configuration file containing blocked domains.
        """
        self.blocked_domains: Set[str] = set(self.DEFAULT_BLOCKED_DOMAINS)
        if config_path:
            self.load_config(config_path)

    def load_config(self, config_path: str) -> None:
        """Load blocked domains from a configuration file.

        Args:
            config_path: Path to the JSON configuration file.

        Raises:
            DomainBlockerError: If the configuration file is invalid or cannot be read.
        """
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                custom_domains = set(config.get('blocked_domains', []))
                self.blocked_domains.update(custom_domains)
        except (json.JSONDecodeError, IOError) as e:
            raise DomainBlockerError(f"Failed to load configuration: {str(e)}")

    def is_domain_blocked(self, url: str) -> bool:
        """Check if a URL's domain is in the blocked list.

        Args:
            url: The URL to check.

        Returns:
            bool: True if the domain is blocked, False otherwise.
        """
        try:
            domain = urlparse(url).netloc.lower()
            # Remove 'www.' prefix if present
            if domain.startswith('www.'):
                domain = domain[4:]
            return any(blocked in domain for blocked in self.blocked_domains)
        except Exception as e:
            raise DomainBlockerError(f"Failed to parse URL: {str(e)}")

    def add_blocked_domain(self, domain: str) -> None:
        """Add a domain to the blocked list.

        Args:
            domain: The domain to block.
        """
        self.blocked_domains.add(domain.lower())

    def remove_blocked_domain(self, domain: str) -> None:
        """Remove a domain from the blocked list.

        Args:
            domain: The domain to unblock.
        """
        try:
            self.blocked_domains.remove(domain.lower())
        except KeyError:
            raise DomainBlockerError(f"Domain {domain} is not in the blocked list")

    def get_blocked_domains(self) -> Set[str]:
        """Get the current set of blocked domains.

        Returns:
            Set[str]: The set of blocked domains.
        """
        return self.blocked_domains.copy()

    def save_config(self, config_path: str) -> None:
        """Save the current blocked domains configuration to a file.

        Args:
            config_path: Path where to save the configuration.

        Raises:
            DomainBlockerError: If the configuration cannot be saved.
        """
        try:
            config = {'blocked_domains': list(self.blocked_domains)}
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=4)
        except IOError as e:
            raise DomainBlockerError(f"Failed to save configuration: {str(e)}")