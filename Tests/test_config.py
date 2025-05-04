import pytest
import os
from Utils.logging_config import get_logger
from Core.exceptions import APIError

logger = get_logger("test_config")


def test_environment_configuration(pytestconfig):
    """
    Verify that the environment configuration option works correctly.
    
    This test checks:
    1. Environment option is present
    2. Environment is one of the expected values
    """
    # Get the environment from config
    env = pytestconfig.getoption('--env')
    
    # Assert that environment is one of the expected values
    assert env in ['staging', 'prod', 'uat'], \
        f"Invalid environment: {env}. Must be staging, production, or development."
    
    # Optional: You can add more specific checks based on your requirements
    print(f"\nTesting with environment: {env}")
    logger.info(f"Testing with environment: {env}")

def test_logging_configuration():
    """
    Verify that logging configuration is set up correctly.
    
    This test checks:
    1. Logging can be configured
    2. Log messages can be generated at different levels
    3. Basic logging functionality
    """
    
    # Try logging at different levels
    try:
        logger.debug("Debug message - should only appear if log level is DEBUG")
        logger.info("Info message - should appear for INFO and lower levels")
        logger.warning("Warning message")
        logger.error("Error message")
        
        # If we reach here, logging is working
        assert True, "Logging configuration successful"
    except Exception as e:
        pytest.fail(f"Logging configuration failed: {e}")

@pytest.mark.integration
@pytest.mark.api
def test_custom_markers_and_fixtures():
    """
    Verify that custom markers are working and can be applied.
    
    This test checks:
    1. Integration marker is recognized
    2. API marker is recognized
    3. Multiple markers can be applied to a single test
    """
    # The markers are already applied to the test function
    # The test will pass if markers are correctly configured
    
    # Optional: You can add custom logic to further verify marker functionality
    markers = list(pytest.mark._markers)
    
    # Check if our custom markers are in the list of registered markers
    assert any('integration' in str(marker) for marker in markers), \
        "Integration marker not properly configured"
    assert any('api' in str(marker) for marker in markers), \
        "API marker not properly configured"
    
    print("\nCustom markers verified successfully")