"""
Unit Tests for Response Utilities (utils/response.py)
This module tests the standardized API response formatting functions
"""
# Import json module to parse JSON responses
import json
# Import the response helper functions to be tested
from utils.response import success_response, error_response


class TestSuccessResponse:
    """
    Test Suite for success_response Function

    This class contains all test cases for the success_response function
    which formats successful API responses.
    """

    def test_success_response_with_data_only(self, app):
        """
        Test success response with data parameter only

        Verifies that a success response is correctly formatted when only
        the data parameter is provided (no custom meta).
        """
        # Create Flask application context for jsonify to work
        with app.app_context():
            # Define test data to be included in the response
            test_data = {'device_id': '123', 'status': 'active'}

            # Call the success_response function with test data
            response, status_code = success_response(data=test_data)

            # Parse the JSON response into a Python dictionary
            response_json = json.loads(response.data)

            # Assert that the HTTP status code is 200 (OK)
            assert status_code == 200, "Status code should be 200 for success"

            # Assert that the 'data' key exists in the response
            assert 'data' in response_json, "Response should contain 'data' key"

            # Assert that the data matches what was passed in
            assert response_json['data'] == test_data, "Response data should match input data"

            # Assert that the 'meta' key exists in the response
            assert 'meta' in response_json, "Response should contain 'meta' key"

            # Assert that meta contains a timestamp field
            assert 'timestamp' in response_json['meta'], "Meta should contain 'timestamp'"

            # Assert that meta contains a request_id field
            assert 'request_id' in response_json['meta'], "Meta should contain 'request_id'"

    def test_success_response_with_custom_meta(self, app):
        """
        Test success response with custom metadata

        Verifies that custom metadata is correctly merged with standard
        meta fields (timestamp and request_id).
        """
        # Create Flask application context
        with app.app_context():
            # Define test data
            test_data = {'message': 'Operation successful'}

            # Define custom metadata to be included
            custom_meta = {'page': 1, 'per_page': 10}

            # Call the success_response function with data and custom meta
            response, status_code = success_response(data=test_data, meta=custom_meta)

            # Parse the JSON response
            response_json = json.loads(response.data)

            # Assert that custom meta fields are present
            assert response_json['meta']['page'] == 1, "Custom meta 'page' should be included"
            assert response_json['meta']['per_page'] == 10, "Custom meta 'per_page' should be included"

            # Assert that standard meta fields are still present
            assert 'timestamp' in response_json['meta'], "Standard 'timestamp' should still be present"
            assert 'request_id' in response_json['meta'], "Standard 'request_id' should still be present"

    def test_success_response_with_none_data(self, app):
        """
        Test success response when data is None

        Verifies that when no data is provided (None), the response
        contains an empty dictionary in the 'data' field.
        """
        # Create Flask application context
        with app.app_context():
            # Call the success_response function with None as data
            response, status_code = success_response(data=None)

            # Parse the JSON response
            response_json = json.loads(response.data)

            # Assert that the HTTP status code is 200
            assert status_code == 200, "Status code should be 200"

            # Assert that data is an empty dictionary when None is passed
            assert response_json['data'] == {}, "Data should be empty dict when None is passed"

    def test_success_response_with_empty_data(self, app):
        """
        Test success response with empty dictionary

        Verifies that an empty dictionary is correctly returned in the response.
        """
        # Create Flask application context
        with app.app_context():
            # Call the success_response function with an empty dictionary
            response, status_code = success_response(data={})

            # Parse the JSON response
            response_json = json.loads(response.data)

            # Assert that data is an empty dictionary
            assert response_json['data'] == {}, "Data should be empty dict"

    def test_success_response_with_list_data(self, app):
        """
        Test success response with list data

        Verifies that list data (e.g., array of items) is correctly
        formatted in the response.
        """
        # Create Flask application context
        with app.app_context():
            # Define test data as a list
            test_data = [{'id': 1, 'name': 'Item 1'}, {'id': 2, 'name': 'Item 2'}]

            # Call the success_response function with list data
            response, status_code = success_response(data=test_data)

            # Parse the JSON response
            response_json = json.loads(response.data)

            # Assert that the data is a list
            assert isinstance(response_json['data'], list), "Data should be a list"

            # Assert that the list has the correct length
            assert len(response_json['data']) == 2, "List should contain 2 items"

            # Assert that the list content matches the input
            assert response_json['data'] == test_data, "List data should match input"


class TestErrorResponse:
    """
    Test Suite for error_response Function

    This class contains all test cases for the error_response function
    which formats error API responses.
    """

    def test_error_response_with_defaults(self, app):
        """
        Test error response with only required parameters

        Verifies that an error response is correctly formatted when only
        the message is provided, using default values for other parameters.
        """
        # Create Flask application context
        with app.app_context():
            # Define the error message
            error_message = "Something went wrong"

            # Call the error_response function with only the message
            response, status_code = error_response(message=error_message)

            # Parse the JSON response
            response_json = json.loads(response.data)

            # Assert that the HTTP status code is 500 (default)
            assert status_code == 500, "Default status code should be 500"

            # Assert that the 'error' key exists in the response
            assert 'error' in response_json, "Response should contain 'error' key"

            # Assert that the error message matches the input
            assert response_json['error']['message'] == error_message, "Error message should match"

            # Assert that the default error code is 'INTERNAL_ERROR'
            assert response_json['error']['code'] == 'INTERNAL_ERROR', "Default code should be 'INTERNAL_ERROR'"

            # Assert that the status in the error object matches the status code
            assert response_json['error']['status'] == 500, "Status should be 500"

            # Assert that details is an empty dictionary by default
            assert response_json['error']['details'] == {}, "Details should be empty dict by default"

            # Assert that meta contains standard fields
            assert 'timestamp' in response_json['meta'], "Meta should contain 'timestamp'"
            assert 'request_id' in response_json['meta'], "Meta should contain 'request_id'"

    def test_error_response_with_custom_code_and_status(self, app):
        """
        Test error response with custom error code and status

        Verifies that custom error codes and HTTP status codes are
        correctly included in the error response.
        """
        # Create Flask application context
        with app.app_context():
            # Define error parameters
            error_message = "Not found"
            error_code = "NOT_FOUND"
            status = 404

            # Call the error_response function with custom parameters
            response, status_code = error_response(
                message=error_message,
                code=error_code,
                status=status
            )

            # Parse the JSON response
            response_json = json.loads(response.data)

            # Assert that the HTTP status code matches the custom status
            assert status_code == 404, "Status code should be 404"

            # Assert that the error code matches the custom code
            assert response_json['error']['code'] == error_code, "Error code should match custom code"

            # Assert that the error message matches
            assert response_json['error']['message'] == error_message, "Error message should match"

            # Assert that the status in the error object matches
            assert response_json['error']['status'] == 404, "Status should be 404"

    def test_error_response_with_details(self, app):
        """
        Test error response with additional error details

        Verifies that additional error details (e.g., validation errors,
        stack traces) are correctly included in the response.
        """
        # Create Flask application context
        with app.app_context():
            # Define error parameters
            error_message = "Validation failed"
            error_code = "VALIDATION_ERROR"
            status = 400
            # Define additional error details
            error_details = {
                'field': 'email',
                'reason': 'Invalid email format'
            }

            # Call the error_response function with details
            response, status_code = error_response(
                message=error_message,
                code=error_code,
                status=status,
                details=error_details
            )

            # Parse the JSON response
            response_json = json.loads(response.data)

            # Assert that the HTTP status code is 400
            assert status_code == 400, "Status code should be 400"

            # Assert that the details match the input
            assert response_json['error']['details'] == error_details, "Error details should match input"

            # Assert that details contain the expected fields
            assert response_json['error']['details']['field'] == 'email', "Details should contain 'field'"
            assert response_json['error']['details']['reason'] == 'Invalid email format', \
                "Details should contain 'reason'"

    def test_error_response_various_status_codes(self, app):
        """
        Test error response with various HTTP status codes

        Verifies that the error_response function correctly handles
        different HTTP status codes (400, 401, 403, 404, 500).
        """
        # Create Flask application context
        with app.app_context():
            # Define a list of test cases with different status codes
            test_cases = [
                (400, "Bad Request", "BAD_REQUEST"),
                (401, "Unauthorized", "UNAUTHORIZED"),
                (403, "Forbidden", "FORBIDDEN"),
                (404, "Not Found", "NOT_FOUND"),
                (500, "Internal Server Error", "INTERNAL_ERROR")
            ]

            # Iterate through each test case
            for status, message, code in test_cases:
                # Call the error_response function for each case
                response, status_code = error_response(
                    message=message,
                    code=code,
                    status=status
                )

                # Parse the JSON response
                response_json = json.loads(response.data)

                # Assert that the status code matches the expected value
                assert status_code == status, f"Status code should be {status}"

                # Assert that the error code matches
                assert response_json['error']['code'] == code, f"Error code should be {code}"

                # Assert that the error message matches
                assert response_json['error']['message'] == message, f"Error message should be {message}"

    def test_error_response_with_none_details(self, app):
        """
        Test error response when details is explicitly None

        Verifies that when details is None, it is converted to an empty dictionary.
        """
        # Create Flask application context
        with app.app_context():
            # Call the error_response function with details=None
            response, status_code = error_response(
                message="Error occurred",
                details=None
            )

            # Parse the JSON response
            response_json = json.loads(response.data)

            # Assert that details is an empty dictionary when None is passed
            assert response_json['error']['details'] == {}, \
                "Details should be empty dict when None is passed"
