"""
Cleanup Fixtures Module

This module provides fixtures for cleaning up test state after test suite execution.
It ensures that the application returns to a known state after tests complete,
regardless of whether they passed or failed.

Key Features:
- Automatic state reset after all tests
- Configurable cleanup operations
- Detailed logging of cleanup actions
- Error handling for cleanup failures

Note: This module assumes the existence of a /reset endpoint in the API
that can restore the application to its initial state.
"""

from typing import Generator, Any
import pytest
from Utils.logging_config import get_logger
import requests
from requests.auth import HTTPBasicAuth
from Conf import api_example_conf as conf

# Configure logger for cleanup operations
logger = get_logger("cleanup_fixtures")


@pytest.fixture(scope="session", autouse=True)
def reset_app_state() -> Generator[None, None, None]:
    """
    Reset application state after all tests complete.
    
    This fixture runs automatically at the end of the test session.
    It calls the API's reset endpoint to restore the application to
    its initial state, ensuring a clean environment for future test runs.
    
    Yields:
        None: This fixture only performs cleanup after tests
        
    Notes:
        - Uses admin credentials for reset operation
        - Logs all cleanup actions and their results
        - Runs even if tests fail to ensure proper cleanup
    """
    # Let all tests run first
    yield
    
    # Reset state after all tests complete
    logger.info("Running cleanup to reset application state after all tests")
    
    # Call the reset endpoint with admin credentials
    auth = HTTPBasicAuth(conf.staging_user, conf.staging_password)
    response = requests.post('http://localhost:5001/reset', auth=auth)
    
    if response.status_code == 200:
        logger.info("Application state has been reset after all tests completed")
    else:
        logger.error(
            f"Failed to reset application state. Status: {response.status_code}"
        )
        logger.error(f"Response: {response.text}") 