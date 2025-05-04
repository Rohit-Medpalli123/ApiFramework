"""
Base URL Configuration

This module contains the base URLs for different environments of the Cars API.
It includes URLs for UI testing, staging, production, and UAT environments.

Note: In a production environment, these URLs should be managed through
environment variables or a configuration management system.
"""

# Type hint for URL strings
from typing import Final

# UI testing base URL
ui_base_url: Final[str] = "https://qxf2.com/"

# API base URLs for different environments
staging_api_base_url: Final[str] = "http://127.0.0.1:5001"  # Local development server
prod_api_base_url: Final[str] = "https://cars-app.qxf2.com"  # Production environment
uat_api_base_url: Final[str] = "https://cars-app.qxf2.com"  # UAT environment
