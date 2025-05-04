"""
Test Results Module
Provides simple test result tracking and reporting.
"""

from typing import Optional, List
from Utils.logging_config import get_logger


class Results:
    """Test result tracking with logging capabilities."""
    
    def __init__(self, log_file_path: Optional[str] = None):
        """
        Initialize test result tracking.
        
        Args:
            log_file_path: Optional path to log file
        """
        self.logger = get_logger("results")
        self.total = 0
        self.passed = 0
        self.failures: List[str] = []
    
    def log(self, message: str) -> None:
        """
        Log an informational message.
        
        Args:
            message: Message to log
        """
        self.logger.info(message)
    
    def success(self, message: str) -> None:
        """
        Log a success message and update counters.
        
        Args:
            message: Success message
        """
        self.logger.info(f"PASS: {message}")
        self.total += 1
        self.passed += 1
    
    def failure(self, message: str) -> None:
        """
        Log a failure message and update counters.
        
        Args:
            message: Failure message
        """
        fail_msg = f"FAIL: {message}"
        self.logger.error(fail_msg)
        self.total += 1
        self.failures.append(fail_msg)
    
    def log_result(
        self, is_success: bool, success_msg: str, failure_msg: str
    ) -> None:
        """
        Log a test result based on success flag.
        
        Args:
            is_success: Whether the test passed
            success_msg: Message for success case
            failure_msg: Message for failure case
        """
        if is_success:
            self.success(success_msg)
        else:
            self.failure(failure_msg)
        self.logger.info("--------")
    
    def get_pass_count(self) -> int:
        """Get the number of passed tests."""
        return self.passed
    
    def get_fail_count(self) -> int:
        """Get the number of failed tests."""
        return self.total - self.passed
    
    def get_pass_percentage(self) -> float:
        """
        Calculate the pass percentage.
        
        Returns:
            float: Percentage of passed tests
        """
        if self.total == 0:
            return 0.0
        return (self.passed / self.total) * 100
    
    def write_test_summary(self) -> None:
        """Write a test summary report."""
        separator = "=" * 20
        
        self.logger.info(f"\n{separator}\n  TEST SUMMARY  \n{separator}")
        self.logger.info(f"Total tests: {self.total}")
        self.logger.info(f"Passed tests: {self.passed}")
        self.logger.info(f"Failed tests: {self.get_fail_count()}")
        self.logger.info(f"Pass rate: {self.get_pass_percentage():.1f}%")
        
        if self.failures:
            self.logger.info("\n--- FAILURES ---")
            for msg in self.failures:
                self.logger.info(msg)
        
        self.logger.info(f"{separator}\n")
