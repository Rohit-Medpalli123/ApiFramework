"""
Configuration Fixtures Module

Provides URL configuration for different test environments.
"""

import pytest
from Conf import base_url_conf


def get_env_url(env):
    """Get URL for the specified environment."""
    # Convert environment name to URL variable name
    url_var_name = f"{env.lower()}_api_base_url"
    # Get URL directly from the config module
    return getattr(base_url_conf, url_var_name)


@pytest.fixture
def base_url(request):
    """Get base URL for testing based on environment."""
    # Get environment from command line or use default
    env = request.config.getoption("--env", default="staging")
    
    # Use environment-specific URL
    return get_env_url(env)


@pytest.fixture
def api_url(base_url):
    """Get complete API endpoint URL."""
    return f"{base_url}"


@pytest.fixture
def testname(request):
    """Get clean test name without parameters."""
    return request.node.name.split('[')[0]



