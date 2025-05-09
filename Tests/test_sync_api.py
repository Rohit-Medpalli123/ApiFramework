"""
API Example Test Suite

This test suite covers the following scenarios for the car API:

1. Add a new car - Verifies that a car can be added successfully.
2. Verify car count - Checks if the car count increases after adding a new car.
3. Update car details - Ensures that car details can be updated.
4. Get car details - Fetches details of a specific car to verify retrieval.
5. Register a car - Tests the registration of a car with customer details.
6. Verify registered cars count - Confirms the count of registered cars.
7. Remove a car - Tests the removal of a car from the system.
8. Verify car deletion - Checks if the car count decreases after deletion.
9. Delete registered car - Ensures a registered car can be deleted.
10. Validation error 403 - Tests for HTTP 403 error with valid auth.
11. Validation error 401 (no auth) - Tests for HTTP 401 error.
12. Validation error 401 (invalid auth) - Tests for HTTP 401 with bad auth.

"""

import os
import sys
import pytest
import allure
from Conf import api_example_conf as conf
from Utils.logging_config import get_logger

# Ensure the project root is in the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logger = get_logger("test_sync_api")

@allure.epic("Cars API Testing Framework")
@allure.feature("Car Management System")
@allure.story("Car Addition")
@allure.description("Test the car addition functionality of the API. This test verifies that a new car can be successfully added to the system with all its details.")
@allure.tag("API", "Cars", "Create")
@allure.severity(allure.severity_level.CRITICAL)
def test_add_car(api_player_fixture, auth_details) -> None:
    """
    Test the car addition functionality of the API.

    Args:
        api_player_fixture: API player with access to all endpoints
        auth_details: Authentication credentials
    """
    # Get car details from configuration
    car_details = conf.car_details
    
    # Use the APIPlayer to add a car
    result_flag, response = api_player_fixture.add_car(
        car_details=car_details,
        auth_details=auth_details
    )
    
    # Log the response
    logger.info(f"Add car response: {response}")
    
    # Assert the operation was successful
    assert result_flag, "Car addition was not successful"
    assert response.get('successful') is True, (
        "Car addition response indicates failure"
    )
    
    # Get the current list of cars to verify the addition
    _, cars_response = api_player_fixture.get_cars(auth_details)
    logger.info(f"Get cars response: {cars_response}")
    
    # Verify the added car exists in the list
    cars_list = cars_response.get('cars_list', [])
    added_car = next(
        (car for car in cars_list 
         if (car['name'] == car_details['name'] and 
             car['brand'] == car_details['brand'])),
        None
    )
    
    assert added_car is not None, (
        f"Added car {car_details['name']} not found in cars list"
    )


@allure.story("Car Count Verification")
@allure.description("Test to verify that the car count increases correctly after adding a new car. This ensures the system's counting mechanism works properly.")
@allure.tag("API", "Cars", "Validation")
@allure.severity(allure.severity_level.NORMAL)
def test_verify_car_count(api_player_fixture, auth_details, initial_car_count):
    """
    Test to verify the car count after adding a new car.
    
    Args:
        api_player_fixture: API player with access to all endpoints
        auth_details: Authentication credentials
        initial_car_count: Initial count of cars from data_fixtures
    """
    # Get the current car count
    current_count = api_player_fixture.get_car_count(auth_details)
    
    # After test_add_car adds one car, we expect initial_count + 1
    expected_count = initial_car_count + 1
    
    # Log the counts
    logger.info(f"Initial count: {initial_car_count}")
    logger.info(f"Current count: {current_count}")
    logger.info(f"Expected count: {expected_count}")
    
    # Assert the counts match
    assert current_count == expected_count, (
        f"Car count incorrect. Expected: {expected_count}, "
        f"Actual: {current_count}"
    )


@allure.story("Car Update")
@allure.description("Test to update the details of an existing car. Verifies that car information can be modified successfully.")
@allure.tag("API", "Cars", "Update")
@allure.severity(allure.severity_level.CRITICAL)
def test_update_car(api_player_fixture, auth_details) -> None:
    """
    Test to update the details of an existing car.

    Args:
        api_player_fixture: API player with access to all endpoints
        auth_details: Authentication credentials
    """
    # Get update details from configuration
    car_name = conf.car_name_2  # This should be 'figo'
    update_car = conf.update_car
    
    # Update the car details
    result_flag, response = api_player_fixture.update_car(
        car_name=car_name,
        car_details=update_car,
        auth_details=auth_details
    )
    
    # Log the response
    logger.info(f"Response for updating car {car_name}: {response}")
    
    # Assert the update was successful
    # The API returns response in {'response': {'successful': true}} format
    if isinstance(response, dict) and 'response' in response:
        response_data = response['response']
        success = response_data.get('successful', False)
        assert success, f"Failed to update car: {car_name}"
    else:
        assert result_flag, f"Failed to update car: {car_name}"
    
    # Verify the update was applied
    _, cars_response = api_player_fixture.get_cars(auth_details)
    updated_car = next(
        (car for car in cars_response.get('cars_list', [])
         if car['name'] == update_car['name']),
        None
    )
    assert updated_car is not None, (
        f"Updated car {update_car['name']} not found"
    )
    assert updated_car['price_range'] == update_car['price_range'], (
        "Car price range was not updated correctly"
    )


@allure.story("Car Details Retrieval")
@allure.description("Test to fetch and verify the details of a specific car. Ensures that car information can be retrieved accurately.")
@allure.tag("API", "Cars", "Read")
@allure.severity(allure.severity_level.NORMAL)
def test_get_car_details(api_player_fixture, auth_details) -> None:
    """
    Test to fetch the details of a specific car.

    Args:
        api_player_fixture: API player with access to all endpoints
        auth_details: Authentication credentials
    """
    # Get car identification details from configuration
    car_name = conf.car_name_1
    brand = conf.brand
    
    # Fetch the car details
    result_flag, response = api_player_fixture.get_car(
        car_name=car_name,
        brand=brand,
        auth_details=auth_details
    )
    
    # Log the response
    logger.info(f"Response for car {car_name}: {response}")
    
    # Assert the fetch was successful
    assert result_flag, f"Failed to fetch details for car: {car_name}"


@allure.story("Car Registration")
@allure.description("Test to register a car with customer details. Verifies the car registration process works correctly.")
@allure.tag("API", "Cars", "Registration")
@allure.severity(allure.severity_level.CRITICAL)
def test_register_car(api_player_fixture, auth_details) -> None:
    """
    Test to register a car with customer details.

    Args:
        api_player_fixture: API player with access to all endpoints
        auth_details: Authentication credentials
    """
    # Get registration details from configuration
    car_name = conf.car_name_1
    brand = conf.brand
    customer_details = conf.customer_details
    
    # Register the car
    result_flag, response = api_player_fixture.register_car(
        car_name=car_name,
        brand=brand,
        auth_details=auth_details
    )
    
    # Log the response
    msg = (f"Response for registering car {car_name} "
           f"with details {customer_details}: {response}")
    logger.info(msg)
    
    # Assert the registration was successful
    assert result_flag, f"Failed to register car: {car_name}"



@allure.story("Registration Count Verification")
@allure.description("Test to verify the count of registered cars. Ensures the registration counting mechanism works properly.")
@allure.tag("API", "Cars", "Validation")
@allure.severity(allure.severity_level.NORMAL)
def test_verify_registration_count(api_player_fixture, auth_details) -> None:
    """
    Test to verify the count of registered cars.

    Args:
        api_player_fixture: API player with access to all endpoints
        auth_details: Authentication credentials
    """
    # Get current registration count with count_only=True
    success, expected_count = api_player_fixture.get_registered_cars(auth_details, count_only=True)
    assert success, "Failed to get registration count"

    # Verify the registration count
    result_flag, actual_count = api_player_fixture.verify_registration_count(
                                   expected_count=expected_count,
                                   auth_details=auth_details)

    # Log the result
    logger.info(f"Expected registrations: {expected_count}, "
                f"Actual: {actual_count}")

    # Assert the counts match
    assert result_flag, (f"Registration count incorrect. "
                        f"Expected: {expected_count}, "
                        f"Actual: {actual_count}")

@allure.story("Registered Car Deletion")
@allure.description("Test to delete a registered car from the system. Verifies that registered cars can be removed properly.")
@allure.tag("API", "Cars", "Delete", "Registration")
@allure.severity(allure.severity_level.CRITICAL)
def test_delete_registered_car(api_player_fixture, auth_details) -> None:
    """
    Test to delete a registered car from the system.
    This test depends on test_register_car having run first and successfully registered a car.

    Args:
        api_player_fixture: API player with access to all endpoints
        auth_details: Authentication credentials
    """
    # Get current registration count
    success, current_count = api_player_fixture.get_registered_cars(auth_details, count_only=True)
    assert success, "Failed to get current registration count"
    assert current_count > 0, "No registered cars found to delete. Ensure test_register_car ran first."
    
    # Delete the registered car
    result_flag, response = api_player_fixture.delete_registered_car(
        auth_details=auth_details
    )
    
    # Log the response
    logger.info(f"Response for deleting registered car: {response}")
    
    # Assert the deletion was successful
    assert result_flag, "Failed to delete registered car"
    assert response.get('successful') is True, "Deletion response indicates failure"
    
    # Verify registration count decreased
    success, final_count = api_player_fixture.get_registered_cars(auth_details, count_only=True)
    assert success, "Failed to get final registration count"
    assert final_count == current_count - 1, "Registration count did not decrease after deletion"


@allure.story("Car Removal")
@allure.description("Test to remove a car from the system. Verifies the car removal operation executes successfully.")
@allure.tag("API", "Cars", "Delete")
@allure.severity(allure.severity_level.CRITICAL)
def test_remove_car(api_player_fixture, auth_details) -> None:
    """
    Test to remove a car from the system.
    This test verifies that the remove operation executes successfully.
    Actual deletion verification is handled by test_verify_car_deletion.

    Args:
        api_player_fixture: API player with access to all endpoints
        auth_details: Authentication credentials
    """
    # Get car name to remove from configuration
    car_name = conf.car_name_2
    
    # Remove the car
    result_flag, response = api_player_fixture.remove_car(
        car_name=car_name,
        auth_details=auth_details
    )
    
    # Log the response
    logger.info(f"Response for removing car {car_name}: {response}")
    
    # Assert the removal operation was successful
    assert result_flag, f"Failed to remove car: {car_name}"
    assert response.get('successful') is True, "Removal response indicates failure"


@allure.story("Car Deletion Verification")
@allure.description("Test to verify the car count and state after deleting a car. Ensures the deletion was successful and system state is consistent.")
@allure.tag("API", "Cars", "Validation", "Delete")
@allure.severity(allure.severity_level.CRITICAL)
def test_verify_car_deletion(api_player_fixture, auth_details, 
                           initial_car_count) -> None:
    """
    Test to verify the car count and state after deleting a car.
    This test depends on test_remove_car having run first and successfully
    removed a car.

    Args:
        api_player_fixture: API player with access to all endpoints
        auth_details: Authentication credentials
        initial_car_count: Initial count of cars before deletion
    """
    # Get current car count directly
    current_count = api_player_fixture.get_car_count(auth_details)
    
    # After test_remove_car removes one car, we expect initial_count - 1
    expected_count = initial_car_count
    
    # Log the counts
    logger.info(f"Initial count: {initial_car_count}")
    logger.info(f"Current count: {current_count}")
    logger.info(f"Expected count: {expected_count}")
    
    # Assert the counts match
    assert current_count == expected_count, (
        f"Car count incorrect after deletion. "
        f"Expected: {expected_count}, Actual: {current_count}"
    )
    
    # Also verify the specific car was removed
    success, cars_response = api_player_fixture.get_cars(auth_details)
    assert success, "Failed to get car list"
    
    cars_list = cars_response.get('cars_list', [])
    car_name = conf.car_name_2  # This should be 'figo'
    removed_car = next(
        (car for car in cars_list if car['name'] == car_name),
        None
    )
    assert removed_car is None, f"Car {car_name} still exists after removal"


@allure.story("Authorization Validation")
@allure.description("Test to verify HTTP 403 error with valid authentication. Ensures proper access control for non-admin users.")
@allure.tag("API", "Security", "Authorization")
@allure.severity(allure.severity_level.BLOCKER)
def test_validation_error_403(api_player_fixture, auth_details) -> None:
    """
    Test to verify HTTP 403 error with valid authentication.
    This test verifies that a non-admin user gets a 403 Forbidden error
    even with valid credentials.

    Args:
        api_player_fixture: API player with access to all endpoints
        auth_details: Authentication credentials
    """
    # Check for validation error with valid auth but non-admin user
    result = api_player_fixture.check_validation_error(auth_details)
    
    # Log the response
    logger.info(f"Validation check result: {result['msg']}")
    
    # Assert we got a 403 error
    assert not result['result_flag'], "Expected validation to fail"
    assert "403 FORBIDDEN" in result['msg'], (
        f"Expected 403 FORBIDDEN error but got: {result['msg']}"
    )


@allure.story("Authentication Validation")
@allure.description("Test to verify HTTP 401 error when no authentication is provided. Ensures system requires authentication.")
@allure.tag("API", "Security", "Authentication")
@allure.severity(allure.severity_level.BLOCKER)
def test_validation_error_401_no_auth(api_player_fixture) -> None:
    """
    Test to verify HTTP 401 error when no authentication is provided.
    This test verifies that requests without authentication credentials
    receive a 401 Unauthorized error.

    Args:
        api_player_fixture: API player with access to all endpoints
    """
    # Check for validation error with no auth
    result = api_player_fixture.check_validation_error(auth_details=None)
    
    # Log the response
    logger.info(f"Validation check result: {result['msg']}")
    
    # Assert we got a 401 error
    assert not result['result_flag'], "Expected validation to fail"
    assert "401 UNAUTHORIZED" in result['msg'], (
        f"Expected 401 UNAUTHORIZED error but got: {result['msg']}"
    )


@allure.story("Invalid Authentication")
@allure.description("Test to verify HTTP 401 error with invalid authentication. Ensures system properly handles invalid credentials.")
@allure.tag("API", "Security", "Authentication")
@allure.severity(allure.severity_level.BLOCKER)
def test_validation_error_401_invalid_auth(api_player_fixture) -> None:
    """
    Test to verify HTTP 401 error with invalid authentication.
    This test verifies that requests with incorrect credentials
    receive a 401 Unauthorized error.

    Args:
        api_player_fixture: API player with access to all endpoints
    """
    # Get invalid credentials from configuration
    username = conf.invalid_user_name
    password = conf.invalid_password
    
    # Generate invalid auth details
    auth_details = api_player_fixture.set_auth_details(username, password)
    
    # Check for validation error with invalid auth
    result = api_player_fixture.check_validation_error(auth_details)
    
    # Log the response
    logger.info(f"Validation check result: {result['msg']}")
    
    # Assert we got a 401 error
    assert not result['result_flag'], "Expected validation to fail"
    assert "401 UNAUTHORIZED" in result['msg'], (
        f"Expected 401 UNAUTHORIZED error but got: {result['msg']}"
    )



   