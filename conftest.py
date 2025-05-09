"""
Pytest configuration and shared fixtures loader.

This file provides centralized configuration and imports fixtures from modular files.
"""

import os
import sys
import pytest
from datetime import datetime

# Add the directory containing the logging configuration to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Import the configurable logging functions
from Utils.logging_config import (
    LoggerConfig,
    add_execution_separator,
    get_logger,
)
from Utils.create_folder import ResultsFolderCreator

# Initialize logger at module level
logger = get_logger("Conftest")

# Global variable to store log file path
_log_file_path = None
_results_folder_path = None


def pytest_addoption(parser):
    """
    Add custom command-line options for pytest.
    
    :param parser: pytest argument parser
    """
    parser.addoption(
        "--env",
        default="staging",
        choices=["staging", "prod", "uat"],
        help="Specify the environment: staging (default), prod, or uat",
    )
    parser.addoption(
        "--log_level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging level",
    )
    parser.addoption(
        '--log-destination', 
        choices=['file', 'reportportal'], 
        default='file',
        help='Destination for logging'
    )
    parser.addoption(
        '--slack_notify',
        action='store_true',
        help='Enable Slack notifications for test results'
    )


def pytest_configure(config):
    """
    Configure pytest run settings.
    
    :param config: pytest configuration object
    """
    # Set custom markers
    config.addinivalue_line(
        "markers", 
        "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", 
        "api: mark test as an API test"
    )
    
    # Store environment option for potential use in tests
    config.option.env = config.getoption("--env")
    
    # Set up HTML report path if not already set
    if not hasattr(config.option, 'htmlpath'):
        results_dir = os.path.join(
            os.path.dirname(__file__),
            'Results'
        )
        os.makedirs(results_dir, exist_ok=True)
        config.option.htmlpath = os.path.join(results_dir, 'report.html')
        logger.info(f"HTML report will be generated at: {config.option.htmlpath}")
    
    # Render the report in a single file
    config.option.self_contained_html = True
    
    # Add environment info to HTML report
    config._metadata = {
        '🚗 Project': 'Cars API Testing',
        '🌍 Environment': config.option.env.upper(),
        '👤 Tester': os.getenv('USER', 'Mystery Tester'),
        '🐍 Python Version': sys.version.split()[0],
        '⏰ Started At': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        '🔧 Test Type': 'API Integration Tests'
    }


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Customize the test report with additional information.
    
    :param item: test item
    :param call: test call
    """
    outcome = yield
    report = outcome.get_result()
    
    # Add test description from docstring
    report.description = str(item.function.__doc__)
    
    # Process the report for all phases (setup, call, teardown)
    if report.when in ["setup", "call", "teardown"]:
        duration = getattr(report, 'duration', 0.0)
        if duration > 60:
            duration_formatted = f"{duration/60:.2f} minutes"
        else:
            duration_formatted = f"{duration:.2f} seconds"
        
        # Initialize extras if not present
        if not hasattr(report, 'extras'):
            report.extras = []
        
        # Add test status with proper color
        status_extra = {
            'name': f'Status ({report.when})',
            'content': report.outcome.upper(),
            'format': 'string',
            'class': {
                'passed': 'green',
                'failed': 'red',
                'skipped': 'yellow'
            }.get(report.outcome, 'gray')
        }
        report.extras.append(status_extra)
        
        # Add duration info
        duration_extra = {
            'name': f'Duration ({report.when})',
            'content': duration_formatted,
            'format': 'string',
            'class': 'blue'
        }
        report.extras.append(duration_extra)
        
        # If there's a failure, add the error message
        if report.failed:
            if hasattr(report, 'longrepr'):
                error_extra = {
                    'name': 'Error Details',
                    'content': str(report.longrepr),
                    'format': 'text',
                    'class': 'red'
                }
                report.extras.append(error_extra)


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """
    Generate additional summary information.
    
    :param terminalreporter: pytest terminal reporter
    :param exitstatus: exit status of the test run
    :param config: pytest configuration object
    """
    # Optional: Custom summary reporting
    if config.getoption("--slack_notify"):
        try:
            # Placeholder for Slack notification implementation
            test_summary = {
                'total': len(terminalreporter.stats.get('call', [])),
                'passed': len(terminalreporter.stats.get('passed', [])),
                'failed': len(terminalreporter.stats.get('failed', [])),
                'skipped': len(terminalreporter.stats.get('skipped', [])),
                'exit_status': exitstatus
            }
            logger.info(f"Test Summary: {test_summary}")
            # Actual Slack notification would be implemented here
            print("Slack notification placeholder: Test summary generated")
        except Exception as e:
            print(f"Error generating Slack notification: {e}")

    # Print log file location if logging was set up
    global _log_file_path, _results_folder_path
    if _log_file_path:
        terminalreporter.write_line(
            f"\nTest logs are available at: {_log_file_path}"
        )
    if _results_folder_path:
        html_report = os.path.join(_results_folder_path, "report.html")
        terminalreporter.write_line(
            f"HTML report is available at: {html_report}"
        )


def get_fixture_modules():
    """
    Dynamically load fixture modules from the Fixtures directory.
    
    :return: List of fixture module paths
    """
    fixtures_dir = os.path.join(os.path.dirname(__file__), 'Fixtures')
    fixture_modules = [
        f'Fixtures.{os.path.splitext(f)[0]}' 
        for f in os.listdir(fixtures_dir) 
        if f.endswith('_fixtures.py') and not f.startswith('__')
    ]
    return fixture_modules


# Register all fixture modules (automatically finds and registers our log fixtures)
pytest_plugins = get_fixture_modules()


def setup_logging(env):
    """
    Set up logging based on pytest configuration.
    
    :param env: Environment to set up logging for
    :return: Boolean indicating success or failure
    """
    try:
        # Create results folder
        logger.info("Creating results folder")
        folder_creator = ResultsFolderCreator(base_path="Results")
        global _results_folder_path
        _results_folder_path = folder_creator.create_exe_results_folders(env)
        logger.info(f"Results folder created at --> {_results_folder_path}")

        # Initialize logging in the results folder
        logger.info("Initializing logging configuration")
        LoggerConfig.setup_logger(_results_folder_path)
        
        # Store the log file path
        global _log_file_path
        _log_file_path = os.path.join(_results_folder_path, "test.log")
            
    except Exception as e:
        logger.error(f"Error during logging setup: {str(e)}")
        return False


# Hook to set up logging before tests run
def pytest_sessionstart(session):
    """
    Hook to set up logging at the start of the pytest session.
    
    :param session: pytest session object
    """
    env = session.config.getoption("--env").upper()
    setup_logging(env)
    
    # Add a separator to the logs
    add_execution_separator(logger, env)
    
    # Log HTML report path
    if hasattr(session.config.option, 'htmlpath'):
        logger.info(f"HTML report configured at: {session.config.option.htmlpath}")
    else:
        logger.warning("HTML report path not configured!")