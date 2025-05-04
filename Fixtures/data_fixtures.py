"""
Data Fixtures Module

Provides fixtures for initializing and managing test data.
Supports retrieving baseline data for test scenarios.

Key Features:
- Initial data state retrieval
- Error-tolerant data fetching
- Flexible test data management
"""

import pytest
from typing import Optional, Dict, Any
import requests
from requests.auth import HTTPBasicAuth


@pytest.fixture(scope='session')
def initial_car_count() -> Optional[int]:
    """
    Get the initial number of cars from the app's initial-count endpoint.
    
    Returns:
        Optional[int]: Initial car count or None if retrieval fails
    
    Notes:
        - Uses direct API call to get initial count
        - Session scoped to get count once for all tests
        - Fails test with descriptive message if count retrieval fails
    """
    try:
        auth = HTTPBasicAuth('qxf2', 'qxf2')
        response = requests.get('http://localhost:5001/initial-count', auth=auth)
        
        if response.status_code == 200:
            return response.json()['count']
        else:
            pytest.fail(
                f"Failed to get initial count. Status: {response.status_code}",
                pytrace=False
            )
    except Exception as e:
        pytest.fail(f"Error getting initial count: {e}", pytrace=False)
