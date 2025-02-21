# archivecli

A command-line interface tool to retrieve archived versions of URLs from archive.is. This tool allows you to quickly access archived versions of web pages using the archive.is service.

## Features

- Retrieve the latest archived version of any URL
- Validate URL format and reachability
- Open archived pages directly in your default browser
- Simple command-line interface

### From Source
```bash
git clone https://github.com/yourusername/archivecli.git
cd archivecli
pip install -e .
```

## Usage

```bash
# Basic usage - retrieve and open archived version of a URL
archive https://example.com

# Run in quiet mode (less output)
archive --quiet https://example.com
```

## Requirements

- Python 3.8 or higher
- Dependencies:
  - requests>=2.28.0
  - click>=8.0.0
  - urllib3>=2.0.0
  - certifi>=2023.7.22

## Development

1. Clone the repository
2. Install development dependencies:
```bash
pip install -r requirements.txt
```
3. Run tests:
```bash
pytest
```

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
