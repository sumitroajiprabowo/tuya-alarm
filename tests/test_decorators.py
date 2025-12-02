"""
Unit Tests for Decorators (utils/decorators.py)
This module tests the Flask route decorators for error handling and validation
"""
# Import json module to parse JSON responses
import json
# Import Flask for creating test routes
from flask import Flask
# Import the decorators to be tested
from utils.decorators import handle_errors, validate_device_id


class TestHandleErrorsDecorator:
    """
    Test Suite for handle_errors Decorator

    This class contains all test cases for the handle_errors decorator
    which wraps Flask routes to catch and format exceptions.
    """

    def test_handle_errors_with_successful_function(self):
        """
        Test handle_errors decorator with a successful function

        Verifies that when a decorated function executes successfully,
        the decorator does not interfere with the normal return value.
        """
        # Create a mock Flask application for testing
        app = Flask(__name__)

        # Define a test route decorated with handle_errors
        @app.route('/test')
        @handle_errors
        def test_route():
            """Test route that returns success"""
            # Return a simple success response
            return {'status': 'success'}, 200

        # Create a test client from the Flask app
        client = app.test_client()

        # Make a GET request to the test route
        response = client.get('/test')

        # Parse the JSON response
        response_json = json.loads(response.data)

        # Assert that the HTTP status code is 200
        assert response.status_code == 200, "Status code should be 200 for successful function"

        # Assert that the response contains the expected data
        assert response_json['status'] == 'success', "Response should contain success status"

    def test_handle_errors_catches_exception(self):
        """
        Test handle_errors decorator catches exceptions

        Verifies that when a decorated function raises an exception,
        the decorator catches it and returns a formatted error response.
        """
        # Create a mock Flask application
        app = Flask(__name__)

        # Define a test route that raises an exception
        @app.route('/test-error')
        @handle_errors
        def test_route_with_error():
            """Test route that raises an exception"""
            # Raise a ValueError to simulate an error
            raise ValueError("Test error message")

        # Create a test client
        client = app.test_client()

        # Make a GET request to the error route
        response = client.get('/test-error')

        # Parse the JSON response
        response_json = json.loads(response.data)

        # Assert that the HTTP status code is 500 (Internal Server Error)
        assert response.status_code == 500, "Status code should be 500 for exception"

        # Assert that the response contains an 'error' key
        assert 'error' in response_json, "Response should contain 'error' key"

        # Assert that the error message matches the raised exception
        assert 'Test error message' in response_json['error']['message'], \
            "Error message should contain the exception message"

        # Assert that the error code is 'INTERNAL_ERROR'
        assert response_json['error']['code'] == 'INTERNAL_ERROR', \
            "Error code should be 'INTERNAL_ERROR'"

    def test_handle_errors_with_different_exception_types(self):
        """
        Test handle_errors with different exception types

        Verifies that the decorator correctly handles various types
        of exceptions (ValueError, KeyError, RuntimeError, etc.).
        """
        # Create a mock Flask application
        app = Flask(__name__)

        # Define test routes for different exception types
        @app.route('/value-error')
        @handle_errors
        def value_error_route():
            """Route that raises ValueError"""
            raise ValueError("Invalid value")

        @app.route('/key-error')
        @handle_errors
        def key_error_route():
            """Route that raises KeyError"""
            raise KeyError("Missing key")

        @app.route('/runtime-error')
        @handle_errors
        def runtime_error_route():
            """Route that raises RuntimeError"""
            raise RuntimeError("Runtime problem")

        # Create a test client
        client = app.test_client()

        # Test ValueError
        response = client.get('/value-error')
        response_json = json.loads(response.data)
        assert response.status_code == 500, "ValueError should return 500"
        assert 'Invalid value' in response_json['error']['message'], \
            "Error message should contain ValueError message"

        # Test KeyError
        response = client.get('/key-error')
        response_json = json.loads(response.data)
        assert response.status_code == 500, "KeyError should return 500"
        assert 'Missing key' in response_json['error']['message'], \
            "Error message should contain KeyError message"

        # Test RuntimeError
        response = client.get('/runtime-error')
        response_json = json.loads(response.data)
        assert response.status_code == 500, "RuntimeError should return 500"
        assert 'Runtime problem' in response_json['error']['message'], \
            "Error message should contain RuntimeError message"

    def test_handle_errors_preserves_function_metadata(self):
        """
        Test that handle_errors preserves function metadata

        Verifies that the @wraps decorator is used correctly,
        preserving the original function's name and docstring.
        """
        # Define a function with specific metadata
        @handle_errors
        def test_function():
            """This is a test function docstring"""
            pass

        # Assert that the function name is preserved
        assert test_function.__name__ == 'test_function', \
            "Function name should be preserved"

        # Assert that the function docstring is preserved
        assert test_function.__doc__ == 'This is a test function docstring', \
            "Function docstring should be preserved"


class TestValidateDeviceIdDecorator:
    """
    Test Suite for validate_device_id Decorator

    This class contains all test cases for the validate_device_id decorator
    which validates device_id parameters in Flask routes.
    """

    def test_validate_device_id_with_valid_id(self):
        """
        Test validate_device_id with a valid device ID

        Verifies that when a valid device_id (length >= 10) is provided,
        the decorator allows the request to proceed normally.
        """
        # Create a mock Flask application
        app = Flask(__name__)

        # Define a test route with device_id parameter
        @app.route('/device/<device_id>')
        @validate_device_id
        def test_route(device_id):
            """Test route that requires device_id"""
            # Return the device_id to confirm it was received
            return {'device_id': device_id}, 200

        # Create a test client
        client = app.test_client()

        # Make a request with a valid device_id (12 characters)
        response = client.get('/device/device123456')

        # Parse the JSON response
        response_json = json.loads(response.data)

        # Assert that the HTTP status code is 200
        assert response.status_code == 200, "Status code should be 200 for valid device_id"

        # Assert that the device_id is correctly passed to the route
        assert response_json['device_id'] == 'device123456', \
            "Device ID should be passed to the route function"

    def test_validate_device_id_with_short_id(self):
        """
        Test validate_device_id with a short device ID

        Verifies that when a device_id shorter than 10 characters is provided,
        the decorator returns a 400 error response.
        """
        # Create a mock Flask application
        app = Flask(__name__)

        # Define a test route with device_id parameter
        @app.route('/device/<device_id>')
        @validate_device_id
        def test_route(device_id):
            """Test route that requires device_id"""
            return {'device_id': device_id}, 200

        # Create a test client
        client = app.test_client()

        # Make a request with a short device_id (9 characters)
        response = client.get('/device/short123')

        # Parse the JSON response
        response_json = json.loads(response.data)

        # Assert that the HTTP status code is 400 (Bad Request)
        assert response.status_code == 400, "Status code should be 400 for short device_id"

        # Assert that the response contains an error
        assert 'error' in response_json, "Response should contain 'error' key"

        # Assert that the error message indicates invalid device_id
        assert 'Invalid device_id' in response_json['error']['message'], \
            "Error message should indicate invalid device_id"

        # Assert that the error code is 'INVALID_PARAM'
        assert response_json['error']['code'] == 'INVALID_PARAM', \
            "Error code should be 'INVALID_PARAM'"

    def test_validate_device_id_with_empty_id(self):
        """
        Test validate_device_id with an empty device ID

        Verifies that when an empty device_id is provided,
        the decorator returns a 400 error response.
        """
        # Create a mock Flask application
        app = Flask(__name__)

        # Define a test route with device_id parameter
        @app.route('/device/<device_id>')
        @validate_device_id
        def test_route(device_id):
            """Test route that requires device_id"""
            return {'device_id': device_id}, 200

        # Create a test client
        client = app.test_client()

        # Make a request with an empty device_id
        response = client.get('/device/')

        # Assert that the HTTP status code is 404 (Not Found)
        # Flask treats missing route parameters as 404
        assert response.status_code == 404, \
            "Status code should be 404 for missing device_id parameter"

    def test_validate_device_id_with_exactly_10_characters(self):
        """
        Test validate_device_id with exactly 10 characters

        Verifies that a device_id with exactly 10 characters (the minimum)
        is considered valid.
        """
        # Create a mock Flask application
        app = Flask(__name__)

        # Define a test route with device_id parameter
        @app.route('/device/<device_id>')
        @validate_device_id
        def test_route(device_id):
            """Test route that requires device_id"""
            return {'device_id': device_id}, 200

        # Create a test client
        client = app.test_client()

        # Make a request with a device_id of exactly 10 characters
        response = client.get('/device/1234567890')

        # Parse the JSON response
        response_json = json.loads(response.data)

        # Assert that the HTTP status code is 200
        assert response.status_code == 200, \
            "Status code should be 200 for 10-character device_id"

        # Assert that the device_id is correctly passed
        assert response_json['device_id'] == '1234567890', \
            "Device ID should be passed correctly"

    def test_validate_device_id_with_special_characters(self):
        """
        Test validate_device_id with special characters

        Verifies that device_ids containing special characters
        are accepted as long as they meet the length requirement.
        """
        # Create a mock Flask application
        app = Flask(__name__)

        # Define a test route with device_id parameter
        @app.route('/device/<device_id>')
        @validate_device_id
        def test_route(device_id):
            """Test route that requires device_id"""
            return {'device_id': device_id}, 200

        # Create a test client
        client = app.test_client()

        # Make a request with a device_id containing special characters
        # Note: URL-unsafe characters need to be percent-encoded
        response = client.get('/device/device-123_456')

        # Parse the JSON response
        response_json = json.loads(response.data)

        # Assert that the HTTP status code is 200
        assert response.status_code == 200, \
            "Status code should be 200 for device_id with special characters"

        # Assert that the device_id is correctly passed
        assert response_json['device_id'] == 'device-123_456', \
            "Device ID with special characters should be accepted"

    def test_validate_device_id_preserves_function_metadata(self):
        """
        Test that validate_device_id preserves function metadata

        Verifies that the @wraps decorator is used correctly,
        preserving the original function's name and docstring.
        """
        # Define a function with specific metadata
        @validate_device_id
        def test_function(device_id):
            """This is a test function with device_id"""
            pass

        # Assert that the function name is preserved
        assert test_function.__name__ == 'test_function', \
            "Function name should be preserved"

        # Assert that the function docstring is preserved
        assert test_function.__doc__ == 'This is a test function with device_id', \
            "Function docstring should be preserved"


class TestDecoratorsCombined:
    """
    Test Suite for Combined Decorators

    This class tests the behavior when multiple decorators are used together,
    which is common in Flask routes.
    """

    def test_both_decorators_with_valid_request(self):
        """
        Test both decorators together with a valid request

        Verifies that when both decorators are applied, they work correctly
        together for valid requests.
        """
        # Create a mock Flask application
        app = Flask(__name__)

        # Define a route with both decorators
        @app.route('/device/<device_id>/action')
        @handle_errors
        @validate_device_id
        def test_route(device_id):
            """Test route with both decorators"""
            return {'device_id': device_id, 'action': 'success'}, 200

        # Create a test client
        client = app.test_client()

        # Make a request with a valid device_id
        response = client.get('/device/device123456/action')

        # Parse the JSON response
        response_json = json.loads(response.data)

        # Assert that the HTTP status code is 200
        assert response.status_code == 200, \
            "Status code should be 200 for valid request with both decorators"

        # Assert that the response contains expected data
        assert response_json['device_id'] == 'device123456', \
            "Device ID should be correct"
        assert response_json['action'] == 'success', \
            "Action should be successful"

    def test_both_decorators_with_invalid_device_id(self):
        """
        Test both decorators with invalid device ID

        Verifies that the validate_device_id decorator properly rejects
        invalid IDs even when handle_errors is also present.
        """
        # Create a mock Flask application
        app = Flask(__name__)

        # Define a route with both decorators
        @app.route('/device/<device_id>/action')
        @handle_errors
        @validate_device_id
        def test_route(device_id):
            """Test route with both decorators"""
            return {'device_id': device_id, 'action': 'success'}, 200

        # Create a test client
        client = app.test_client()

        # Make a request with an invalid device_id (too short)
        response = client.get('/device/short/action')

        # Parse the JSON response
        response_json = json.loads(response.data)

        # Assert that the HTTP status code is 400
        assert response.status_code == 400, \
            "Status code should be 400 for invalid device_id"

        # Assert that the response contains an error
        assert 'error' in response_json, \
            "Response should contain error for invalid device_id"

    def test_both_decorators_with_exception_in_route(self):
        """
        Test both decorators when route raises exception

        Verifies that handle_errors properly catches exceptions even when
        validate_device_id is also applied.
        """
        # Create a mock Flask application
        app = Flask(__name__)

        # Define a route that raises an exception
        @app.route('/device/<device_id>/error')
        @handle_errors
        @validate_device_id
        def test_route(device_id):
            """Test route that raises exception"""
            # Raise an exception to test error handling
            raise ValueError("Simulated error")

        # Create a test client
        client = app.test_client()

        # Make a request with a valid device_id but route raises error
        response = client.get('/device/device123456/error')

        # Parse the JSON response
        response_json = json.loads(response.data)

        # Assert that the HTTP status code is 500
        assert response.status_code == 500, \
            "Status code should be 500 for exception"

        # Assert that the error is properly formatted
        assert 'error' in response_json, \
            "Response should contain error"
        assert 'Simulated error' in response_json['error']['message'], \
            "Error message should contain the exception message"