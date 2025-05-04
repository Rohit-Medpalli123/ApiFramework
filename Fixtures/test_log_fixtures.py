"""
Test Logging Fixtures

This module provides fixtures for enhancing test logs with separators 
and other visual enhancements.
"""

import pytest
from Utils.logging_config import get_logger

logger = get_logger("test_logs")


@pytest.fixture(autouse=True)
def log_separator_after_test():
    """
    Add a visual separator after each test to make logs more readable.
    
    This fixture is automatically applied to all tests due to autouse=True.
    It yields control during test execution and then adds a separator
    to the log once the test has completed.
    """
    # This code runs before each test
    yield
    # This code runs after each test completes
    
    # Add a separator line to visually distinguish between tests 
    logger.info(f"\n" + "=" * 80 + f"\n✅ TEST COMPLETED\n" + "=" * 80 + "\n")