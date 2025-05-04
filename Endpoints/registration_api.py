"""
API methods for /registration endpoint
"""
from typing import Any, Dict
from .base_api import BaseAPI
from Utils.logging_config import get_logger
from Core.exceptions import APIError

logger = get_logger("RegistrationAPIEndpoints")


class RegistrationAPIEndpoints(BaseAPI):
    """Class to handle API interactions related to car registration."""

    def __init__(self, base_url: str) -> None:
        """
        Initialize RegistrationAPIEndpoints with a base URL.
        
        Args:
            base_url: The base URL for the registration API
        """
        super().__init__(base_url)
        self.endpoint = "register"

    def get_url(self, suffix: str = "") -> str:
        """
        Generate the full URL for registration API endpoints.
        
        Args:
            suffix: Additional path to append to the URL
            
        Returns:
            Complete URL string
        """
        return self.build_url(self.endpoint, suffix)

    def register_car(
        self,
        params: Dict[str, Any],
        json: Dict[str, Any],
        headers: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Registers a car with the system.
        
        Args:
            params: Query parameters (car_name and brand)
            json: Registration details
            headers: Request headers
            
        Returns:
            Response from the API
            
        Raises:
            APIError: If the request fails
        """
        url = self.get_url("/car")
        response, error = self.post(url, params=params, json=json, headers=headers)
        return self.format_response(url, response, error)

    def get_registered_cars(
        self,
        headers: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Retrieves the list of registered cars.
        
        Args:
            headers: Request headers
            
        Returns:
            Response from the API
            
        Raises:
            APIError: If the request fails
        """
        url = self.get_url("")
        response, error = self.get(url, headers=headers)
        return self.format_response(url, response, error)

    def delete_registered_car(
        self,
        headers: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Deletes a registered car.
        
        Args:
            headers: Request headers
            
        Returns:
            Response from the API
            
        Raises:
            APIError: If the request fails
        """
        url = self.get_url("/car/delete")
        response, error = self.delete(url, headers=headers)
        return self.format_response(url, response, error)

    # Async Methods
    async def get_registered_cars_async(
        self,
        headers: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Asynchronously retrieves the list of registered cars.
        
        Args:
            headers: Request headers
            
        Returns:
            Response from the API
            
        Raises:
            APIError: If the request fails
        """
        url = self.get_url("/list")
        response, error = await self.async_get(url, headers=headers)
        return self.format_response(url, response, error)
