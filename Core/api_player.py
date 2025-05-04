# pylint: disable=line-too-long
"""
APIPlayer class:
a) Serves as a test orchestrator for API tests
b) Directly interfaces with endpoint classes for API calls
c) Maintains test context and tracks test results
"""

from base64 import b64encode
import json
from typing import Optional, Tuple, Dict, Any, Callable, Union
from Core.exceptions import APIAuthenticationError, APINotFoundError
from Endpoints.cars_api import CarsAPIEndpoints
from Endpoints.registration_api import RegistrationAPIEndpoints
from Endpoints.users_api import UserAPIEndpoints
from Utils.results import Results
from Utils.logging_config import get_logger


class APIPlayer(Results):
    """Maintains test context/state and orchestrates API test operations."""

    def __init__(self, url: str, log_file_path: Optional[str] = None, 
                 environment: str = "staging", logger=None):
        """
        Initializes APIPlayer with endpoint classes.
        
        Args:
            url: Base URL for API endpoints
            log_file_path: Path to log file
            environment: Environment name (staging, prod, etc.)
            logger: Custom logger if provided
        """
        # Initialize the Results class with proper parameters
        super().__init__(log_file_path=log_file_path)
        
        # Store environment for potential use
        self.environment = environment
        
        # Use provided logger if available, otherwise create one
        self.logger = get_logger("APIPlayer")
        
        self.logger.info(f"🔧 Initializing APIPlayer with base URL: {url} in {environment} environment")
            
        # Directly create endpoint class instances
        self.cars_api = CarsAPIEndpoints(url)
        self.users_api = UserAPIEndpoints(url)
        self.registration_api = RegistrationAPIEndpoints(url)
        
        self.logger.info("✅ APIPlayer initialization complete")

    def set_auth_details(self, username: str, password: str) -> str:
        """
        Encodes authentication details for basic auth.
        
        Args:
            username: API username
            password: API password
            
        Returns:
            Base64 encoded credentials
        """
        self.logger.info(f"🔐 Generating auth token for user: {username}")
        b64login = b64encode(bytes(f"{username}:{password}", "utf-8"))
        return b64login.decode("utf-8")

    def set_header_details(self, auth_details: Optional[str] = None) -> Dict[str, str]:
        """
        Creates headers with or without authentication details.
        
        Args:
            auth_details: Optional base64 encoded auth string
            
        Returns:
            Headers dictionary
        """
        if auth_details:
            self.logger.info("📨 Creating authenticated headers")
            return {'Authorization': f"Basic {auth_details}"}
        
        self.logger.info("📨 Creating non-authenticated headers")
        return {'content-type': 'application/json'}

    def _execute_api_call(self, operation_name: str, api_lambda: Callable) -> Tuple[bool, Dict[str, Any]]:
        """
        Executes an API call with consistent logging and result tracking.
        
        Args:
            operation_name: Name of the operation for logging
            api_lambda: Lambda function that executes the API call
            
        Returns:
            Tuple containing success flag and response data
        """
        self.logger.info(f"🚀 STARTING OPERATION: {operation_name}")
        
        # Execute the API call using the lambda
        self.logger.info(f"📡 Sending request for {operation_name}")
        response = api_lambda()
        
        # Extract the actual response data
        response_data = response.get('response', {})
        status_code = response.get('status_code')
        
        # Log response summary
        self.logger.info(f"📥 Received response for {operation_name} with status: {status_code}")
        
        # Determine if the operation was successful
        result_flag = response_data.get("successful", False)
        
        # Log the result
        if result_flag:
            self.success(f"✅ Successfully executed {operation_name}")
        else:
            self.failure(f"❌ Failed to execute {operation_name}")
            
        self.logger.info(f"🏁 COMPLETED OPERATION: {operation_name}\n")
        return result_flag, response_data

    # Core API operations with consistent error handling and logging
    def get_cars(self, auth_details: Optional[str] = None) -> Tuple[bool, Dict[str, Any]]:
        """
        Fetches the list of available cars.
        
        Args:
            auth_details: Optional authentication string
            
        Returns:
            Tuple of (success_flag, response_data)
        """
        self.logger.info("➡️ Starting get_cars operation")
        headers = self.set_header_details(auth_details)
        
        self.logger.info(f"📝 Request parameters: headers={headers}")
        
        return self._execute_api_call(
            "get_cars", 
            lambda: self.cars_api.get_cars(headers=headers)
        )

    def get_car(self, car_name: str, brand: str, 
                auth_details: Optional[str] = None) -> Tuple[bool, Dict[str, Any]]:
        """
        Fetches details of a specific car.
        
        Args:
            car_name: Name of the car
            brand: Brand of the car
            auth_details: Optional authentication string
            
        Returns:
            Tuple of (success_flag, response_data)
        """
        self.logger.info(f"➡️ Starting get_car operation for {car_name} ({brand})")
        params = {'car_name': car_name, 'brand': brand}
        headers = self.set_header_details(auth_details)
        
        self.logger.info(f"📝 Request parameters: params={params}, headers={headers}")
        
        return self._execute_api_call(
            f"get_car({car_name})", 
            lambda: self.cars_api.get_car(params=params, headers=headers)
        )

    def add_car(self, car_details: Dict[str, Any], 
                auth_details: Optional[str] = None) -> Tuple[bool, Dict[str, Any]]:
        """
        Adds a new car to the system.
        
        Args:
            car_details: Car details dictionary
            auth_details: Optional authentication string
            
        Returns:
            Tuple of (success_flag, response_data)
        """
        self.logger.info("➡️ Starting add_car operation")
        headers = self.set_header_details(auth_details)
        
        # Pretty print car details for better logging
        car_details_str = json.dumps(car_details, indent=2)
        self.logger.info(f"📝 Request parameters: \ncar_details={car_details_str}\nheaders={headers}")
        
        return self._execute_api_call(
            "add_car", 
            lambda: self.cars_api.add_car(data=car_details, headers=headers)
        )

    def register_car(self, car_name: str, brand: str, 
                     auth_details: Optional[str] = None) -> Tuple[bool, Dict[str, Any]]:
        """
        Registers a car to the system.
        
        Args:
            car_name: Name of the car
            brand: Brand of the car
            auth_details: Optional authentication string
            
        Returns:
            Tuple of (success_flag, response_data)
        """
        from Conf import api_example_conf as conf
        
        self.logger.info(f"➡️ Starting register_car operation for {car_name} ({brand})")
        params = {'car_name': car_name, 'brand': brand}
        headers = self.set_header_details(auth_details)
        
        # Pretty print customer details for better logging
        customer_details_str = json.dumps(conf.customer_details, indent=2)
        self.logger.info(f"📝 Request parameters: \nparams={params}\ncustomer_details={customer_details_str}\nheaders={headers}")
        
        result_flag, response = self._execute_api_call(
            f"register_car({car_name})",
            lambda: self.registration_api.register_car(
                params=params,
                json=conf.customer_details,
                headers=headers
            )
        )
        
        # Special case - registration response has a different structure
        self.logger.info("🔍 Extracting registration success status from response")
        result_flag = response.get("registered_car", {}).get("successful", False)
        return result_flag, response

    def update_car(self, car_details: Dict[str, Any], car_name: str = 'figo', 
                   auth_details: Optional[str] = None) -> Tuple[bool, Dict[str, Any]]:
        """
        Updates car details.
        
        Args:
            car_details: Updated car details
            car_name: Name of the car to update
            auth_details: Optional authentication string
            
        Returns:
            Tuple of (success_flag, response_data)
        """
        self.logger.info(f"➡️ Starting update_car operation for {car_name}")
        headers = self.set_header_details(auth_details)
        
        # Pretty print car details for better logging
        car_details_str = json.dumps(car_details, indent=2)
        self.logger.info(f"📝 Request parameters: \ncar_name={car_name}\ncar_details={car_details_str}\nheaders={headers}")
        
        return self._execute_api_call(
            f"update_car({car_name})",
            lambda: self.cars_api.update_car(
                car_name=car_name,
                data=car_details,
                headers=headers
            )
        )

    def remove_car(self, car_name: str, 
                   auth_details: Optional[str] = None) -> Tuple[bool, Dict[str, Any]]:
        """
        Removes a car from the system.
        
        Args:
            car_name: Name of the car to remove
            auth_details: Optional authentication string
            
        Returns:
            Tuple of (success_flag, response_data)
        """
        self.logger.info(f"➡️ Starting remove_car operation for {car_name}")
        headers = self.set_header_details(auth_details)
        
        self.logger.info(f"📝 Request parameters: car_name={car_name}, headers={headers}")
        
        return self._execute_api_call(
            f"remove_car({car_name})",
            lambda: self.cars_api.remove_car(
                car_name=car_name,
                headers=headers
            )
        )

    def get_registered_cars(
        self, 
        auth_details: Optional[str] = None,
        count_only: bool = False
    ) -> Union[Tuple[bool, Dict[str, Any]], Tuple[bool, int]]:
        """
        Fetches the list of registered cars or their count.
        
        Args:
            auth_details: Optional authentication string
            count_only: If True, returns only the count of registered cars
            
        Returns:
            If count_only is False:
                Tuple of (success_flag, response_data)
            If count_only is True:
                Tuple of (success_flag, count)
        """
        self.logger.info(
            "🔢 Getting registered car count" if count_only
            else "➡️ Starting get_registered_cars operation"
        )
        
        headers = self.set_header_details(auth_details)
        self.logger.info(f"📝 Request parameters: headers={headers}")
        
        success, response = self._execute_api_call(
            "get_registered_cars",
            lambda: self.registration_api.get_registered_cars(headers=headers)
        )
        
        if count_only:
            count = len(response.get('registered', [])) if success else 0
            self.logger.info(f"🔢 Found {count} registered cars")
            return success, count
            
        return success, response

    def delete_registered_car(self, 
                              auth_details: Optional[str] = None) -> Tuple[bool, Dict[str, Any]]:
        """
        Deletes registered cars.
        
        Args:
            auth_details: Optional authentication string
            
        Returns:
            Tuple of (success_flag, response_data)
        """
        self.logger.info("➡️ Starting delete_registered_car operation")
        headers = self.set_header_details(auth_details)
        
        self.logger.info(f"📝 Request parameters: headers={headers}")
        
        return self._execute_api_call(
            "delete_registered_car",
            lambda: self.registration_api.delete_registered_car(headers=headers)
        )

    def reset_app_state(self, auth_details: Optional[str] = None) -> Dict[str, Any]:
        """
        Resets the application state to initial values.
        
        Args:
            auth_details: Optional authentication string
            
        Returns:
            Response from the API
        """
        self.logger.info("➡️ Starting reset_app_state operation")
        headers = self.set_header_details(auth_details)
        
        self.logger.info(f"📝 Request parameters: headers={headers}")
        
        try:
            self.logger.info("📡 Sending request to reset application state")
            response = self.cars_api.reset_app_state(headers=headers)
            self.logger.info(f"📥 Received reset response: {response}")
            return response
        except Exception as e:
            self.logger.error(f"❌ Error resetting application state: {e}")
            return {"error": str(e)}

    def get_user_list(self, 
                      auth_details: Optional[str] = None) -> Tuple[bool, Dict[str, Any]]:
        """
        Gets the list of users.
        
        Args:
            auth_details: Optional authentication string
            
        Returns:
            Tuple of (success_flag, response_data)
        """
        self.logger.info("➡️ Starting get_user_list operation")
        headers = self.set_header_details(auth_details)
        
        self.logger.info(f"📝 Request parameters: headers={headers}")
        
        try:
            self.logger.info("📡 Sending request to users API")
            response = self.users_api.get_user_list(headers=headers)
            self.logger.info(f"📥 Received user list response: {response}")
            return True, response
        except (TypeError, AttributeError) as e:
            self.logger.error(f"❌ Error fetching user list: {e}")
            return False, {}

    # Test orchestration methods
    def get_car_count(self, auth_details: Optional[str] = None) -> int:
        """
        Gets the total car count.
        
        Args:
            auth_details: Optional authentication string
            
        Returns:
            Number of cars
        """
        self.logger.info("🔢 Getting car count")
        _, response = self.get_cars(auth_details)
        count = len(response.get('cars_list', []))
        self.logger.info(f"🔢 Found {count} cars")
        return count

    def verify_car_count(self, expected_count: int, 
                         auth_details: Optional[str] = None) -> Tuple[bool, int]:
        """
        Verifies if the car count matches the expected count.
        
        Args:
            expected_count: Expected number of cars
            auth_details: Optional authentication string
            
        Returns:
            Tuple of (success_flag, actual_count)
        """
        self.logger.info(f"🔍 Verifying car count, expecting {expected_count}")
        actual_count = self.get_car_count(auth_details)
        result_flag = actual_count == expected_count
        
        self.logger.info(f"🔍 Car count verification: expected {expected_count}, actual {actual_count}")
        
        if result_flag:
            self.success("✅ Car count matches expected count")
        else:
            self.failure(f"❌ Car count does not match: expected {expected_count}, got {actual_count}")
            
        return result_flag, actual_count

    def verify_registration_count(self, expected_count: int, 
                                  auth_details: Optional[str] = None) -> Tuple[bool, int]:
        """
        Verifies if the registered car count matches the expected count.
        
        Args:
            expected_count: Expected number of registered cars
            auth_details: Optional authentication string
            
        Returns:
            Tuple of (success_flag, actual_count)
        """
        self.logger.info(f"🔍 Verifying registered car count, expecting {expected_count}")
        actual_count = self.get_registered_cars(auth_details, count_only=True)[1]
        result_flag = actual_count == expected_count
        
        if result_flag:
            self.success("✅ Registered car count matches expected count")
        else:
            self.failure(f"❌ Registered car count does not match: expected {expected_count}, got {actual_count}")
            
        return result_flag, actual_count

    def check_validation_error(self, 
                           auth_details: Optional[str] = None) -> Dict[str, Any]:
        """
        Checks validation error and returns the appropriate message.
        
        Args:
            auth_details: Optional authentication string
            
        Returns:
            Dictionary with result flag and message
        """
        self.logger.info("🔍 Checking validation errors")
        result_flag = False
        response_code = None
        
        try:
            success, result = self.get_user_list(auth_details)
            if success and result.get('successful', False):
                response_code = 200
            else:
                # If we get a response but it's not successful, it's a 403
                response_code = 403
        except APIAuthenticationError:
            response_code = 401
        except APINotFoundError:
            response_code = 404
        except Exception as e:
            self.logger.error(f"❌ Unexpected error: {e}")
            return {'result_flag': False, 'msg': str(e)}
        
        error_messages = {
            403: "403 FORBIDDEN: Authentication successful but no access for non-admin users",
            200: "Successful authentication and access permission",
            401: "401 UNAUTHORIZED: Authenticate with proper credentials OR Require Basic Auth",
            404: "404 NOT FOUND: URL not found",
        }

        msg = error_messages.get(response_code, "Unknown reason")
        if response_code == 200:
            result_flag = True
        self.logger.info(f"🔍 Validation check result: {msg}")
        return {'result_flag': result_flag, 'msg': msg}

    # Async methods for performance testing
    async def async_get_cars(self, 
                             auth_details: Optional[str] = None) -> Tuple[bool, Dict[str, Any]]:
        """
        Fetches available cars asynchronously.
        
        Args:
            auth_details: Optional authentication string
            
        Returns:
            Tuple of (success_flag, response_data)
        """
        self.logger.info("🔄 Starting async_get_cars operation")
        headers = self.set_header_details(auth_details)
        
        self.logger.info("📡 Sending async request to cars API")
        response = await self.cars_api.get_cars_async(headers)
        result_flag = response.status_code == 200

        self.logger.info(f"📥 Async get_cars response: status={response.status_code}")
        return result_flag, response.json()

    async def async_get_car(self, car_name: str, brand: str, 
                            auth_details: Optional[str] = None) -> Tuple[bool, Dict[str, Any]]:
        """
        Gets a specific car asynchronously.
        
        Args:
            car_name: Name of the car
            brand: Brand of the car
            auth_details: Optional authentication string
            
        Returns:
            Tuple of (success_flag, response_data)
        """
        self.logger.info(f"🔄 Starting async_get_car operation for {car_name}")
        params = {'car_name': car_name, 'brand': brand}
        headers = self.set_header_details(auth_details)
        
        self.logger.info(f"📡 Sending async request to get car {car_name}")
        response = await self.cars_api.get_car_async(params=params, headers=headers)
        result_flag = response.status_code == 200

        self.logger.info(f"📥 Async get_car response: status={response.status_code}")
        return result_flag, response.json()

    async def async_add_car(self, car_details: Dict[str, Any], 
                            auth_details: Optional[str] = None) -> Tuple[bool, Dict[str, Any]]:
        """
        Adds a new car asynchronously.
        
        Args:
            car_details: Car details dictionary
            auth_details: Optional authentication string
            
        Returns:
            Tuple of (success_flag, response_data)
        """
        self.logger.info("🔄 Starting async_add_car operation")
        headers = self.set_header_details(auth_details)
        
        car_details_str = json.dumps(car_details, indent=2)
        self.logger.info(f"📡 Sending async request to add car: {car_details_str}")
        response = await self.cars_api.add_car_async(data=car_details, headers=headers)
        result_flag = response.status_code == 200

        self.logger.info(f"📥 Async add_car response: status={response.status_code}")
        return result_flag, response.json()

    async def async_get_registered_cars(self, 
                                        auth_details: Optional[str] = None) -> Tuple[bool, Dict[str, Any]]:
        """
        Fetches registered cars asynchronously.
        
        Args:
            auth_details: Optional authentication string
            
        Returns:
            Tuple of (success_flag, response_data)
        """
        self.logger.info("🔄 Starting async_get_registered_cars operation")
        headers = self.set_header_details(auth_details)
        
        self.logger.info("📡 Sending async request to get registered cars")
        response = await self.registration_api.get_registered_cars_async(headers=headers)
        result_flag = response.status_code == 200

        self.logger.info(f"📥 Async get_registered_cars response: status={response.status_code}")
        return result_flag, response.json()
