"""
A base class for making RESTful API calls using the Requests library.
Provides connection pooling, retry mechanisms, and custom error handling.
"""

import asyncio
import logging
import requests
from requests.exceptions import HTTPError, RequestException
from typing import Any, Dict, Optional, Tuple
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from Core.exceptions import (
    APIError,
    APIRequestError,
    APIConnectionError,
    APIAuthenticationError,
    APINotFoundError,
    APIRateLimitError
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure retry strategy
retry_strategy = Retry(
    total=3,  # number of retries
    backoff_factor=1,  # wait 1, 2, 4 seconds between retries
    status_forcelist=[429, 500, 502, 503, 504]  # HTTP status codes to retry on
)

class BaseAPI:
    """
    A base class for making RESTful API calls using the Requests library.
    Provides connection pooling, retry mechanisms, and custom error handling.
    """
    
    def __init__(self, base_url: str, timeout: int = 30):
        """
        Initialize the BaseAPI with a required base URL.
        
        Args:
            base_url: The base URL for the API
            timeout: Request timeout in seconds (default: 30)
        """
        self.base_url = base_url
        self.session = requests.Session()
        self.session.timeout = timeout
        
        # Configure connection pooling and retry strategy
        adapter = HTTPAdapter(
            max_retries=retry_strategy,
            pool_connections=10,
            pool_maxsize=10
        )
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def __del__(self):
        """Clean up session resources when the object is destroyed."""
        if hasattr(self, 'session'):
            self.session.close()

    def build_url(self, endpoint: str, suffix: str = "") -> str:
        """
        Build a complete URL for an endpoint.
        :param endpoint: The API endpoint (e.g., 'cars', 'users')
        :param suffix: Additional path or query parameters
        :return: Complete URL
        """
        return f"{self.base_url}/{endpoint}{suffix}"

    def _handle_error(self, error: Exception, method: str, url: str) -> None:
        """
        Handle API errors and raise appropriate custom exceptions.
        
        Args:
            error: The exception that occurred
            method: HTTP method used
            url: URL that was requested
            
        Raises:
            Appropriate APIError subclass based on the error
        """
        if isinstance(error, HTTPError):
            status_code = error.response.status_code
            if status_code == 401:
                raise APIAuthenticationError(f"Authentication failed for {method} {url}")
            elif status_code == 403:
                raise APIAuthenticationError(f"Access forbidden for {method} {url}")
            elif status_code == 404:
                raise APINotFoundError(f"Resource not found at {method} {url}")
            elif status_code == 429:
                raise APIRateLimitError(f"Rate limit exceeded for {method} {url}")
            elif status_code >= 500:
                raise APIRequestError(
                    f"Server error for {method} {url}",
                    status_code=status_code,
                    response=error.response.json() if error.response else None
                )
            else:
                raise APIRequestError(
                    f"Request failed for {method} {url}",
                    status_code=status_code,
                    response=error.response.json() if error.response else None
                )
        elif isinstance(error, RequestException):
            raise APIConnectionError(f"Connection error for {method} {url}: {str(error)}")
        else:
            raise APIError(f"Unexpected error for {method} {url}: {str(error)}")

    def request(self, method: str, url: str, **kwargs) -> Tuple[Optional[requests.Response], Optional[str]]:
        """
        Generic method to make an HTTP request with error handling.
        :param method: HTTP method (GET, POST, PUT, DELETE)
        :param url: API endpoint URL
        :param kwargs: Additional request parameters
        :return: Tuple containing Response object or None, and error message if any
        """
        try:
            response = self.session.request(method=method, url=url, **kwargs)
            response.raise_for_status()
            return response, None
        except Exception as e:
            self._handle_error(e, method, url)
            return None, str(e)

    def get(self, url: str, **kwargs) -> Tuple[Optional[requests.Response], Optional[str]]:
        """ Perform a GET request. """
        return self.request("GET", url, **kwargs)

    def post(self, url: str, **kwargs) -> Tuple[Optional[requests.Response], Optional[str]]:
        """ Perform a POST request. """
        return self.request("POST", url, **kwargs)

    def put(self, url: str, **kwargs) -> Tuple[Optional[requests.Response], Optional[str]]:
        """ Perform a PUT request. """
        return self.request("PUT", url, **kwargs)

    def delete(self, url: str, **kwargs) -> Tuple[Optional[requests.Response], Optional[str]]:
        """ Perform a DELETE request. """
        return self.request("DELETE", url, **kwargs)

    async def async_request(self, method: str, url: str, **kwargs) -> Tuple[Optional[requests.Response], Optional[str]]:
        """ Perform an asynchronous request using threading. """
        return await asyncio.to_thread(self.request, method, url, **kwargs)

    async def async_get(self, url: str, **kwargs) -> Tuple[Optional[requests.Response], Optional[str]]:
        """ Perform an asynchronous GET request. """
        return await self.async_request("GET", url, **kwargs)

    async def async_post(self, url: str, **kwargs) -> Tuple[Optional[requests.Response], Optional[str]]:
        """ Perform an asynchronous POST request. """
        return await self.async_request("POST", url, **kwargs)

    async def async_put(self, url: str, **kwargs) -> Tuple[Optional[requests.Response], Optional[str]]:
        """ Perform an asynchronous PUT request. """
        return await self.async_request("PUT", url, **kwargs)

    async def async_delete(self, url: str, **kwargs) -> Tuple[Optional[requests.Response], Optional[str]]:
        """ Perform an asynchronous DELETE request. """
        return await self.async_request("DELETE", url, **kwargs)

    def format_response(self, url: str, response: Optional[requests.Response], error: Optional[str]) -> Dict[str, Any]:
        """
        Format the response in a consistent way.
        :param url: The URL that was requested
        :param response: The Response object from the request
        :param error: Error message, if any
        :return: Formatted response dictionary
        """
        if response:
            try:
                return {
                    "url": url,
                    "response": response.json(),
                    "error": None,
                    "status_code": response.status_code
                }
            except ValueError:
                return {
                    "url": url,
                    "response": None,
                    "error": "Invalid JSON response",
                    "status_code": response.status_code
                }
        return {
            "url": url,
            "response": None,
            "error": error,
            "status_code": None
        }

    def _handle_response(
        self, 
        response: requests.Response, 
        expected_status: Optional[int] = None
    ) -> Dict[str, Any]:
        """Handle the API response and raise appropriate exceptions.
        
        Args:
            response: The response object from the request
            expected_status: Expected HTTP status code (optional)
            
        Returns:
            Dict containing the parsed response data
            
        Raises:
            Various API exceptions based on the response status
        """
        try:
            response.raise_for_status()
            
            if (expected_status and 
                response.status_code != expected_status):
                msg = (
                    f"Expected status {expected_status} "
                    f"but got {response.status_code}"
                )
                raise APIError(msg)
                
            return response.json()
            
        except HTTPError as e:
            status_code = response.status_code
            error_msg = (
                f"HTTP {status_code}: "
                f"{str(e)}"
            )
            
            if status_code == 404:
                raise APINotFoundError(error_msg)
            elif status_code == 401:
                raise APIAuthenticationError(error_msg) 
            elif status_code == 429:
                raise APIRateLimitError(error_msg)
            else:
                raise APIRequestError(error_msg)
                
        except RequestException as e:
            msg = (
                f"Failed to connect to API: "
                f"{str(e)}"
            )
            raise APIConnectionError(msg)
            
        except Exception as e:
            msg = f"Unexpected error: {str(e)}"
            raise APIError(msg)

    async def _make_async_request(
        self,
        method: str,
        endpoint: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Make an asynchronous HTTP request.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            **kwargs: Additional request parameters
            
        Returns:
            Dict containing the parsed response data
        """
        loop = asyncio.get_event_loop()
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            response = await loop.run_in_executor(
                None,
                lambda: self.session.request(
                    method, 
                    url, 
                    **kwargs
                )
            )
            return self._handle_response(response)
            
        except Exception as e:
            msg = (
                f"Async request failed: {method} {url} - "
                f"{str(e)}"
            )
            raise APIError(msg)
