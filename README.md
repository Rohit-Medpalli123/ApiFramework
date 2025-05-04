# API Testing Framework

A robust, extensible Python framework for API testing with support for both synchronous and asynchronous requests.

## Features

- **Flexible Request Handling**: Support for both sync and async HTTP requests
- **Comprehensive Error Handling**: Custom exception hierarchy for different API errors
- **Automatic Retries**: Built-in retry mechanism for transient failures
- **Authentication Support**: Handles various authentication methods
- **Modular Design**: Easy to extend and customize for different APIs
- **Logging**: Detailed logging for requests and responses
- **Type Hints**: Full type annotation support for better IDE integration

## Project Structure

```
ApiFramework/
├── Core/
│   ├── api_interface.py    # Base interface for API interactions
│   ├── api_player.py       # Main orchestrator for API operations
│   └── exceptions.py       # Custom exception hierarchy
├── Endpoints/
│   ├── base_api.py        # Base API implementation
│   ├── cars_api.py        # Cars API specific endpoints
│   ├── registration_api.py # Registration specific endpoints
│   └── users_api.py       # User management endpoints
├── Utils/
│   ├── logging_config.py  # Logging configuration
│   ├── results.py        # Test result tracking
│   └── create_folder.py  # File system utilities
└── Tests/
    └── test_sync_api.py  # API test suite
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ApiFramework
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Example

```python
from Core.api_player import APIPlayer
from Endpoints.cars_api import CarsAPIEndpoints

# Initialize API player
api_player = APIPlayer()

# Set authentication
auth_details = api_player.set_auth_details("username", "password")

# Create endpoint instance
cars_api = CarsAPIEndpoints(api_player)

# Make API calls
response = cars_api.get_cars(auth_details)
```

### Async Example

```python
import asyncio
from Core.api_player import AsyncAPIPlayer

async def main():
    api_player = AsyncAPIPlayer()
    auth_details = await api_player.set_auth_details("username", "password")
    cars_api = CarsAPIEndpoints(api_player)
    response = await cars_api.get_cars_async(auth_details)

asyncio.run(main())
```

## Error Handling

The framework provides a comprehensive exception hierarchy:

- `APIError`: Base exception for all API-related errors
  - `APIRequestError`: General request failures
  - `APIConnectionError`: Network connectivity issues
  - `APIAuthenticationError`: Authentication failures
  - `APIValidationError`: Request validation failures
  - `APINotFoundError`: Resource not found (404)
  - `APIRateLimitError`: Rate limit exceeded

Example:
```python
try:
    response = cars_api.get_cars(auth_details)
except APIAuthenticationError:
    print("Authentication failed")
except APIConnectionError as e:
    print(f"Connection error: {e}")
```

## Configuration

The framework supports various configuration options:

- Retry settings
- Timeout configuration
- Base URLs for different environments
- Authentication methods
- Logging levels and formats

Example configuration:
```python
api_player = APIPlayer(
    base_url="https://api.example.com",
    max_retries=3,
    retry_delay=1,
    timeout=30
)
```

## Testing

Run the test suite:
```bash
pytest Tests/
```

With coverage:
```bash
pytest --cov=. Tests/
```

## Logging

The framework provides detailed logging:

```python
from Utils.logging_config import LoggerConfig

# Setup logging
LoggerConfig.setup_logger("logs")

# Logs will include:
# - Request details (URL, method, headers)
# - Response status and content
# - Error details and stack traces
# - Performance metrics
```

## Best Practices

1. **Error Handling**: Always wrap API calls in try-except blocks
2. **Authentication**: Store credentials securely, never hardcode
3. **Validation**: Validate responses using the provided methods
4. **Logging**: Enable appropriate logging for debugging
5. **Testing**: Write comprehensive tests for new endpoints
6. **Type Hints**: Maintain type hints for better code quality

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
