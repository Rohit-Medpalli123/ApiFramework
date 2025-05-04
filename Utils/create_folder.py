"""
Results Folder Creator Module

This module provides functionality for creating and managing test result folders.
It organizes results in a hierarchical structure based on date, environment,
and execution timestamp.

Folder Structure:
    Results/
    └── DD-MM-YYYY/
        └── ENV/
            └── HH-MM-SS/

Example:
    creator = ResultsFolderCreator()
    result_path = creator.create_exe_results_folders('staging')
    # Creates: Results/01-01-2024/staging/14-30-00/
"""

from datetime import datetime
import os
from typing import Final


class ResultsFolderCreator:
    """Creates and manages hierarchical folder structures for test results."""

    # Default format strings for date and time
    _DATE_FORMAT: Final[str] = '%d-%m-%Y'
    _TIME_FORMAT: Final[str] = '%H-%M-%S'

    def __init__(self, base_path: str = "Results") -> None:
        """
        Initialize the ResultsFolderCreator.

        Args:
            base_path: Root directory for storing results folders.
                      Defaults to 'Results' in current directory.
        """
        self.base_path = base_path

    def _create_folder(self, folder_path: str) -> None:
        """
        Create a folder if it does not exist.

        Args:
            folder_path: Absolute or relative path for the folder.

        Note:
            Uses exist_ok=True to handle concurrent folder creation
            gracefully.
        """
        os.makedirs(folder_path, exist_ok=True)

    def create_exe_results_folders(self, env: str) -> str:
        """
        Create timestamped results folders for a specific environment.

        Creates a hierarchical folder structure:
        base_path/current_date/environment/timestamp/

        Args:
            env: Environment name (e.g., 'staging', 'production')

        Returns:
            Path to the created timestamp folder

        Example:
            >>> creator = ResultsFolderCreator('Results')
            >>> path = creator.create_exe_results_folders('staging')
            >>> print(path)
            'Results/01-01-2024/staging/14-30-00'
        """
        # Create date-based folder
        current_date_folder = os.path.join(
            self.base_path,
            datetime.now().strftime(self._DATE_FORMAT)
        )
        self._create_folder(current_date_folder)
        
        # Create environment-specific folder
        client_folder_path = os.path.join(current_date_folder, str(env))
        self._create_folder(client_folder_path)
        
        # Create timestamp-based folder
        timestamp_folder_path = os.path.join(
            client_folder_path,
            datetime.now().strftime(self._TIME_FORMAT)
        )
        self._create_folder(timestamp_folder_path)
        
        return timestamp_folder_path
