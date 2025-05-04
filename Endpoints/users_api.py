"""
API methods for /users endpoint
"""
from typing import Any, Dict
from .base_api import BaseAPI
from Utils.logging_config import get_logger
from Core.exceptions import APIError

logger = get_logger("UserAPIEndpoints")


class UserAPIEndpoints(BaseAPI):
    """Class to handle API interactions related to users."""

    def __init__(self, base_url: str) -> None:
        """
        Initialize UserAPIEndpoints with a base URL.
        
        Args:
            base_url: The base URL for the users API
        """
        super().__init__(base_url)
        self.endpoint = "users"

    def get_url(self, suffix: str = "") -> str:
        """
        Generate the full URL for users API endpoints.
        
        Args:
            suffix: Additional path to append to the URL
            
        Returns:
            Complete URL string
        """
        return self.build_url(self.endpoint, suffix)

    def get_user_list(
        self,
        headers: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Retrieves the list of users.
        
        Args:
            headers: Request headers
            
        Returns:
            Response from the API
            
        Raises:
            APIError: If the request fails
        """
        url = self.get_url()  # The endpoint is just /users
        response, error = self.get(url, headers=headers)
        return self.format_response(url, response, error)

    def add_user(
        self,
        data: Dict[str, Any],
        headers: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Adds a new user.
        
        Args:
            data: User details to add
            headers: Request headers
            
        Returns:
            Response from the API
            
        Raises:
            APIError: If the request fails
        """
        url = self.get_url("/add")
        response, error = self.post(url, json=data, headers=headers)
        return self.format_response(url, response, error)

    def update_user(
        self,
        user_id: str,
        data: Dict[str, Any],
        headers: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Updates a user's details.
        
        Args:
            user_id: ID of the user to update
            data: New user details
            headers: Request headers
            
        Returns:
            Response from the API
            
        Raises:
            APIError: If the request fails
        """
        url = self.get_url(f"/update/{user_id}")
        response, error = self.put(url, json=data, headers=headers)
        return self.format_response(url, response, error)

    def delete_user(
        self,
        user_id: str,
        headers: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Deletes a user.
        
        Args:
            user_id: ID of the user to delete
            headers: Request headers
            
        Returns:
            Response from the API
            
        Raises:
            APIError: If the request fails
        """
        url = self.get_url(f"/delete/{user_id}")
        response, error = self.delete(url, headers=headers)
        return self.format_response(url, response, error)

    # Async Methods
    async def get_user_list_async(
        self,
        headers: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Asynchronously retrieves the list of users.
        
        Args:
            headers: Request headers
            
        Returns:
            Response from the API
            
        Raises:
            APIError: If the request fails
        """
        url = self.get_url()  # The endpoint is just /users
        response, error = await self.async_get(url, headers=headers)
        return self.format_response(url, response, error)
