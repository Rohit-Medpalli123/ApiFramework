"""
Custom exceptions for API error handling.
"""

class APIError(Exception):
    """Base exception for all API-related errors."""
    pass


class APIRequestError(APIError):
    """Exception raised when an API request fails."""
    def __init__(self, message: str, status_code: int = None, response: dict = None):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(self.message)


class APIConnectionError(APIError):
    """Exception raised when there's a connection error."""
    pass


class APIValidationError(APIError):
    """Exception raised when API validation fails."""
    pass


class APIAuthenticationError(APIError):
    """Exception raised when authentication fails."""
    pass


class APINotFoundError(APIError):
    """Exception raised when a resource is not found."""
    pass


class APIRateLimitError(APIError):
    """Exception raised when rate limit is exceeded."""
    pass 