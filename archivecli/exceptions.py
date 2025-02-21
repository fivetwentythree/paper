"""Custom exceptions for the archivecli tool.

This module defines a hierarchy of custom exceptions used throughout the archivecli tool
to provide clear error handling and user feedback.
"""

class ArchiveCliError(Exception):
    """Base exception class for all archivecli errors.
    
    All other exceptions in the tool should inherit from this class.
    This allows catching any archivecli-specific error with a single except clause.
    """
    pass


class URLError(ArchiveCliError):
    """Base class for URL-related errors.
    
    Used for any errors related to URL handling, validation, or processing.
    """
    pass


class URLValidationError(URLError):
    """Raised when URL validation fails.
    
    This could be due to invalid format, missing scheme, or other validation issues.
    """
    pass


class URLReachabilityError(URLError):
    """Raised when a URL cannot be reached.
    
    This could be due to network issues, DNS problems, or the server being down.
    """
    pass


class ArchiveServiceError(ArchiveCliError):
    """Base class for archive.is service related errors.
    
    Used for any errors that occur while interacting with the archive.is service.
    """
    pass


class ArchiveNotFoundError(ArchiveServiceError):
    """Raised when no archive is found for a URL.
    
    This indicates that archive.is has no saved version of the requested URL.
    """
    pass


class ArchiveCreationError(ArchiveServiceError):
    """Raised when creating a new archive fails.
    
    This could be due to service issues, rate limiting, or other archive.is errors.
    """
    pass


class ArchiveServiceUnavailableError(ArchiveServiceError):
    """Raised when the archive.is service is unavailable.
    
    This could be due to maintenance, server issues, or network problems.
    """
    pass


class BrowserError(ArchiveCliError):
    """Raised when there are issues with browser operations.
    
    This could be due to browser launch failures or other browser-related issues.
    """
    pass


class ConfigurationError(ArchiveCliError):
    """Raised when there are configuration-related issues.
    
    This could be due to invalid settings, missing configuration files, etc.
    """
    pass