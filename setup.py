import os
from setuptools import setup, find_packages

# Read version from package __init__.py
def get_version():
    init_path = os.path.join(os.path.dirname(__file__), "archivecli", "__init__.py")
    with open(init_path) as f:
        for line in f:
            if line.startswith("__version__"):
                return line.split("=")[1].strip().strip('"\'')
    return "0.1.0"

# Read long description from README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="archivecli",
    version=get_version(),
    packages=find_packages(exclude=["tests*"]),
    install_requires=[
        "requests>=2.28.0",
        "click>=8.0.0",
        "urllib3>=2.0.0",
        "certifi>=2023.7.22"
    ],
    entry_points={
        "console_scripts": [
            "archive=archivecli.cli:main",
        ],
    },
    author="Lochana Perera",
    author_email="loki.l.perera@gmail.com",
    description="A CLI tool to retrieve archived versions of URLs from archive.is",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/archivecli",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/archivecli/issues",
        "Documentation": "https://github.com/yourusername/archivecli#readme",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    keywords="archive web-archive cli url-archiver archive.is",
    include_package_data=True,
    zip_safe=False,
)