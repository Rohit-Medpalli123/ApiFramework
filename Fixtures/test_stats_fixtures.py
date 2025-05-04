"""
Test Statistics Fixtures

This module provides fixtures for collecting and reporting test statistics.
It is designed to be automatically used in pytest sessions.
"""

import pytest
from Utils.logging_config import get_logger

logger = get_logger("test_stats")


@pytest.fixture(scope="session", autouse=True)
def log_test_stats(request):
    """
    Session-level fixture that logs test statistics after all tests complete.
    
    This fixture is automatically used in all test sessions due to 
    autouse=True. It collects information about passed and failed tests 
    and generates a comprehensive report at the end of the test session.
    
    Args:
        request: pytest request object with session information
    """
    # This code runs before any tests
    yield
    # This code runs after all tests complete
    
    # Get test report and log the summary
    logger.info("\n\n🔍 TEST SESSION COMPLETED")
    logger.info("=" * 50)
    
    # Get test outcome counts
    total = getattr(request.session, 'testscollected', 0)
    
    # Handle different pytest versions (testsfailed can be a list or an int)
    failed = 0
    if hasattr(request.session, 'testsfailed'):
        if isinstance(request.session.testsfailed, int):
            failed = request.session.testsfailed
        else:
            failed = len(request.session.testsfailed)
    
    passed = total - failed
    
    # Calculate and log statistics
    pass_rate = 0
    if total > 0:
        pass_rate = (passed / total) * 100
    
    logger.info(f"Total tests: {total}")
    logger.info(f"Passed tests: {passed}")
    logger.info(f"Failed tests: {failed}")
    logger.info(f"Pass rate: {pass_rate:.1f}%")
    
    # Log failures if any (may not have details in some pytest versions)
    has_failure_details = (hasattr(request.session, 'testsfailed') and
                            not isinstance(request.session.testsfailed, int))
    
    if failed > 0 and has_failure_details:
        logger.info("\n🔴 FAILURES:")
        for i, failed_test in enumerate(request.session.testsfailed, 1):
            logger.info(f"{i}. {failed_test.nodeid}")
    
    logger.info("=" * 50) 