"""
API methods for /cars endpoint
"""
from typing import Any, Dict, Optional, Tuple
from .base_api import BaseAPI
from Utils.logging_config import get_logger
from Core.exceptions import APIError

logger = get_logger("CarsAPIEndpoints")


class CarsAPIEndpoints(BaseAPI):
    """Class to handle API interactions related to cars."""

    def __init__(self, base_url: str) -> None:
        """
        Initialize CarsAPIEndpoints with a base URL.
        
        Args:
            base_url: The base URL for the cars API
        """
        super().__init__(base_url)
        self.endpoint = "cars"

    def get_url(self, suffix: str = "") -> str:
        """
        Generate the full URL for cars API endpoints.
        
        Args:
            suffix: Additional path to append to the URL
            
        Returns:
            Complete URL string
        """
        return self.build_url(self.endpoint, suffix)

    def add_car(
        self,
        data: Dict[str, Any],
        headers: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Adds a new car.
        
        Args:
            data: Car details to add
            headers: Request headers
            
        Returns:
            Response from the API
            
        Raises:
            APIError: If the request fails
        """
        url = self.get_url("/add")
        logger.info(f"Adding car with URL: {url}")
        response, error = self.post(url, json=data, headers=headers)
        return self.format_response(url, response, error)

    def get_cars(self, headers: Dict[str, str]) -> Dict[str, Any]:
        """
        Retrieves the list of cars.
        
        Args:
            headers: Request headers
            
        Returns:
            Response from the API
            
        Raises:
            APIError: If the request fails
        """
        url = self.get_url()
        logger.info(f"URL: {url}")
        response, error = self.get(url, headers=headers)
        logger.info(f"Response: {response.text}")
        return self.format_response(url, response, error)

    def get_car(
        self,
        params: Dict[str, Any],
        headers: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Retrieves details of a specific car.
        
        Args:
            params: Query parameters (car_name and brand)
            headers: Request headers
            
        Returns:
            Response from the API
            
        Raises:
            APIError: If the request fails
        """
        url = self.get_url("/find")
        response, error = self.get(url, params=params, headers=headers)
        logger.info(f"Response: {response.text}")
        return self.format_response(url, response, error)

    def update_car(
        self,
        car_name: str,
        data: Dict[str, Any],
        headers: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Updates a given car.
        
        Args:
            car_name: Name of the car to update
            data: New car details
            headers: Request headers
            
        Returns:
            Response from the API
            
        Raises:
            APIError: If the request fails
        """
        url = self.get_url(f"/update/{car_name}")
        logger.info(f"URL: {url}")
        response, error = self.put(url, json=data, headers=headers)
        
        # Log response details
        if error:
            logger.error(f"Error occurred: {error}")
        if response:
            logger.info(f"Response Status Code: {response.status_code}")
            logger.info(f"Response Body: {response.text}")
        
        return self.format_response(url, response, error)

    def remove_car(
        self,
        car_name: str,
        headers: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Deletes a car entry.
        
        Args:
            car_name: Name of the car to remove
            headers: Request headers
            
        Returns:
            Response from the API
            
        Raises:
            APIError: If the request fails
        """
        url = self.get_url(f"/remove/{car_name}")
        response, error = self.delete(url, headers=headers)
        return self.format_response(url, response, error)

    def reset_app_state(
        self,
        headers: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Resets the application state to its initial values.
        
        Args:
            headers: Request headers
            
        Returns:
            Response from the API
            
        Raises:
            APIError: If the request fails
        """
        url = self.base_url + "/reset"
        logger.info(f"Resetting application state with URL: {url}")
        response, error = self.post(url, headers=headers)
        
        # Log response details
        if error:
            logger.error(f"Error resetting application state: {error}")
        if response:
            logger.info(f"Reset Status Code: {response.status_code}")
            logger.info(f"Reset Response: {response.text}")
        
        return self.format_response(url, response, error)

    # Async Methods
    async def get_cars_async(
        self,
        headers: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Asynchronously gets the list of cars.
        
        Args:
            headers: Request headers
            
        Returns:
            Response from the API
            
        Raises:
            APIError: If the request fails
        """
        url = self.get_url()
        response, error = await self.async_get(url, headers=headers)
        return self.format_response(url, response, error)
    
    async def add_car_async(
        self,
        data: Dict[str, Any],
        headers: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Asynchronously add a new car.
        
        Args:
            data: Car details to add
            headers: Request headers
            
        Returns:
            Response from the API
            
        Raises:
            APIError: If the request fails
        """
        url = self.get_url("/add")
        response, error = await self.async_post(url, json=data, headers=headers)
        return self.format_response(url, response, error)

    async def get_car_async(
        self,
        params: Dict[str, Any],
        headers: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Asynchronously get car details using params.
        
        Args:
            params: Query parameters (car_name and brand)
            headers: Request headers
            
        Returns:
            Response from the API
            
        Raises:
            APIError: If the request fails
        """
        url = self.get_url("/find")
        response, error = await self.async_get(url, params=params, headers=headers)
        return self.format_response(url, response, error)
