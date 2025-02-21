"""Command-line interface for archivecli.

This module provides the command-line interface for the archivecli tool,
integrating URL validation, archive service, and browser handling components.
"""

import sys
import argparse
import logging
from typing import List, Optional

from .validators import validate_url_with_reachability
from .archive_service import ArchiveService
from .browser_handler import open_url_in_browser
from .exceptions import (
    URLReachabilityError,
    URLValidationError,
    ArchiveServiceError,
    ArchiveNotFoundError,
    ArchiveServiceUnavailableError,
    ArchiveCreationError,
    BrowserError,
    ConfigurationError
)
from .logging_config import configure_logging, get_logger

__version__ = "0.1.0"

# Module-level logger
logger = get_logger(__name__)


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser.

    Returns:
        argparse.ArgumentParser: Configured argument parser
    """
    parser = argparse.ArgumentParser(
        description="A command-line tool to find and open archived versions of web pages.",
        epilog="Example: archivecli https://example.com"
    )
    
    parser.add_argument(
        "url",
        help="URL to find in archive"
    )
    
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"archivecli {__version__}"
    )
    
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="suppress non-error output"
    )
    
    return parser


def log_message(message: str, level: int = logging.INFO) -> None:
    """Log a message at the specified level.

    Args:
        message: The message to log
        level: The logging level to use (default: INFO)
    """
    logger.log(level, message)


def main(argv: Optional[List[str]] = None) -> int:
    """Main entry point for the CLI.

    Args:
        argv: List of command line arguments (defaults to sys.argv[1:])

    Returns:
        int: Exit code (0 for success, non-zero for errors)
    """
    parser = create_parser()
    args = parser.parse_args(argv)
    
    # Configure logging based on quiet flag
    configure_logging(quiet=args.quiet)
    
    try:
        # Validate URL
        logger.info(f"Validating URL: {args.url}")
        validated_url = validate_url_with_reachability(args.url)
        logger.debug(f"URL validated successfully: {validated_url}")
        
        # Find archived version
        logger.info("Searching for archived version...")
        archive_service = ArchiveService()
        archive_url = archive_service.get_latest_archive(validated_url)
        logger.debug(f"Found archive URL: {archive_url}")
        
        # Open in browser
        logger.info(f"Opening archived version: {archive_url}")
        success, message = open_url_in_browser(archive_url)
        
        if not success:
            logger.error(f"Failed to open browser: {message}")
            return 1
        
        logger.info("Operation completed successfully")
        return 0
        
    except URLValidationError as e:
        print(f"Error: Invalid URL format - {str(e)}", file=sys.stderr)
        return 2
    except URLReachabilityError as e:
        print(f"Error: Could not reach URL - {str(e)}", file=sys.stderr)
        return 3
    except ArchiveNotFoundError:
        print(f"Error: No archived version found for {args.url}", file=sys.stderr)
        print("Tip: You can try again later as the page might be archived in the future.", file=sys.stderr)
        return 4
    except ArchiveServiceUnavailableError as e:
        print(f"Error: Archive.is service unavailable - {str(e)}", file=sys.stderr)
        print("Tip: Please wait a few minutes and try again.", file=sys.stderr)
        return 5
    except ArchiveCreationError as e:
        print(f"Error: Could not create archive - {str(e)}", file=sys.stderr)
        return 6
    except ArchiveServiceError as e:
        print(f"Error: Archive service error - {str(e)}", file=sys.stderr)
        return 7
    except BrowserError as e:
        print(f"Error: Could not open browser - {str(e)}", file=sys.stderr)
        print("Tip: Try setting your default browser or manually visit the archive URL.", file=sys.stderr)
        return 8
    except ConfigurationError as e:
        print(f"Error: Configuration error - {str(e)}", file=sys.stderr)
        return 9
    except Exception as e:
        print(f"Error: An unexpected error occurred - {str(e)}", file=sys.stderr)
        print("This is likely a bug. Please report it to the developers.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())