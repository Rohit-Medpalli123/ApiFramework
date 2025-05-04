"""
API Test Configuration

This module contains configuration values for testing the Cars API.
It includes test data for cars, customer details, and authentication credentials.

Note: In a production environment, sensitive data like passwords should be stored
in environment variables or secure configuration management systems.
"""

from typing import Dict, Any

# Car details for adding a new car
car_details: Dict[str, str] = {
    'name': 'figo',
    'brand': 'Ford',
    'price_range': '2-3lacs',
    'car_type': 'hatchback'
}

# Car details for get_car_details test
car_name_1: str = 'Swift'
brand: str = 'Maruti'

# Car details for update test
car_name_2: str = 'figo'
update_car: Dict[str, str] = {
    'name': 'figo',
    'brand': 'Ford',
    'price_range': '5-10lacs',
    'car_type': 'hatchback'
}

# Customer details for car registration
customer_details: Dict[str, str] = {
    'customer_name': 'Rohit',
    'city': 'BLR'
}

# Default authentication credentials (non-admin user)
user_name: str = 'eric'
password: str = 'testqxf2'

# Environment-specific authentication credentials
staging_user: str = 'qxf2'       # Admin user
staging_password: str = 'qxf2'
prod_user: str = 'admin'          # Admin user
prod_password: str = 'admin123'
dev_user: str = 'dev'             # Non-admin user
dev_password: str = 'dev123'

# Invalid authentication details for negative testing
invalid_user_name: str = 'unknown'
invalid_password: str = 'unknown'