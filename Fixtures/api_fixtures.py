"""
API Fixtures Module

This module provides pytest fixtures for API-related test setup and configuration.
It manages the creation and lifecycle of APIPlayer instances for test scenarios.

Key Responsibilities:
- Create APIPlayer instances for each test
- Provide consistent API access across test cases
- Handle API player initialization and cleanup
"""

import pytest
import logging
from typing import Generator, Optional
from Core.api_player import APIPlayer

# Configure module-level logging
logger = logging.getLogger(__name__)

@pytest.fixture(scope='function')
def api_player_fixture(
                        request: pytest.FixtureRequest, 
                        api_url: str
                    ) -> Generator[APIPlayer, None, None]:
    """
    Creates an APIPlayer instance for each test function.

    This fixture ensures that:
    - A fresh APIPlayer is created for each test
    - Proper error handling during initialization
    - Optional environment-specific configuration

    Args:
        request (pytest.FixtureRequest): Pytest request object providing test context
        api_url (str): Base URL for the API endpoint

    Yields:
        APIPlayer: Configured APIPlayer instance ready for test use

    Raises:
        Exception: If APIPlayer initialization fails
    """
    try:
        # Retrieve environment from CLI options
        env: str = request.config.getoption("--env", default="staging")
        
        # Create APIPlayer with comprehensive configuration
        test_api_obj: APIPlayer = APIPlayer(
                                            url=api_url,
                                            logger=logger,
                                            environment=env
                                        )
        
        # Log fixture setup for traceability
        logger.info(f"APIPlayer initialized for test: {request.node.name}")
        
        # Yield the fixture for test consumption
        yield test_api_obj
        
    except Exception as e:
        # Enhanced error logging with full stack trace
        logger.error(
            f"APIPlayer initialization failed for test {request.node.name}: {e}", 
            exc_info=True
        )
        raise
    finally:
        # Perform cleanup operations if necessary
        logger.info(f"APIPlayer fixture teardown for test: {request.node.name}")
