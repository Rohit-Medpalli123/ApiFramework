"""
APIInterface acts as a composed interface for all API endpoint objects.
It provides an abstraction layer for accessing different endpoint classes.
"""

from Endpoints.cars_api import CarsAPIEndpoints
from Endpoints.registration_api import RegistrationAPIEndpoints
from Endpoints.users_api import UserAPIEndpoints
from Utils.logging_config import get_logger


class APIInterface:
    """
    APIInterface composes multiple API endpoint classes.
    Provides a central access point to all endpoints through delegation.
    """

    def __init__(self, url):
        """
        Initialize the APIInterface with endpoint objects.
        
        Args:
            url: The base URL for API interactions
        """
        self.base_url = url
        self.logger = get_logger("APIInterface")
        
        # Composition: Create instances of each endpoint class
        self.cars = CarsAPIEndpoints(url)
        self.users = UserAPIEndpoints(url)
        self.registration = RegistrationAPIEndpoints(url)
    
    # Cars API delegated methods
    def get_cars(self, headers=None):
        """Get list of cars."""
        return self.cars.get_cars(headers=headers)
    
    def get_car(self, params=None, headers=None):
        """Get details of a specific car."""
        return self.cars.get_car(params=params, headers=headers)
    
    def add_car(self, data=None, headers=None):
        """Add a new car."""
        return self.cars.add_car(data=data, headers=headers)
    
    def update_car(self, car_name=None, data=None, headers=None):
        """Update an existing car."""
        return self.cars.update_car(
            car_name=car_name, 
            data=data, 
            headers=headers
        )
    
    def remove_car(self, car_name=None, headers=None):
        """Remove a car."""
        return self.cars.remove_car(car_name=car_name, headers=headers)
    
    # Registration API delegated methods
    def register_car(self, params=None, json=None, headers=None):
        """Register a car."""
        return self.registration.register_car(
            params=params, 
            json=json, 
            headers=headers
        )
    
    def get_registered_cars(self, headers=None):
        """Get list of registered cars."""
        return self.registration.get_registered_cars(headers=headers)
    
    def delete_registered_car(self, headers=None):
        """Delete a registered car."""
        return self.registration.delete_registered_car(headers=headers)
    
    # Users API delegated methods
    def get_user_list(self, headers=None):
        """Get list of users."""
        return self.users.get_user_list(headers=headers)
    
    # Async methods
    async def get_cars_async(self, headers=None):
        """Get cars asynchronously."""
        return await self.cars.get_cars_async(headers=headers)
    
    async def get_car_async(self, params=None, headers=None):
        """Get car details asynchronously."""
        return await self.cars.get_car_async(params=params, headers=headers)
    
    async def add_car_async(self, data=None, headers=None):
        """Add car asynchronously."""
        return await self.cars.add_car_async(data=data, headers=headers)
    
    async def get_registered_cars_async(self, headers=None):
        """Get registered cars asynchronously."""
        return await self.registration.get_registered_cars_async(
            headers=headers
        )
