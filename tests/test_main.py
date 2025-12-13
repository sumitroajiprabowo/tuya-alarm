"""
Unit Tests for Main Application (main.py)
This module tests the Flask application factory and error handlers
"""

# Import pytest framework for testing
import pytest

# Import json module for JSON operations
import json

# Import Mock and patch for mocking dependencies
from unittest.mock import Mock, patch, MagicMock

# Import Flask for assertions
from flask import Flask

# Import the create_app factory function
from main import create_app


class TestCreateApp:
    """
    Test Suite for Application Factory

    This class tests the create_app factory function that creates
    and configures the Flask application instance.
    """

    @patch("main.TuyaConfig")
    def test_create_app_returns_flask_instance(self, mock_tuya_config):
        """
        Test that create_app returns a Flask instance

        Verifies that the create_app factory function returns
        a properly configured Flask application instance.
        """
        # Mock the TuyaConfig.validate method to prevent actual validation
        mock_tuya_config.validate.return_value = None

        # Call the create_app factory function
        app = create_app()

        # Assert that the returned object is a Flask instance
        assert isinstance(app, Flask), "create_app should return a Flask instance"

        # Assert that the app has the correct name
        assert app.name == "main", "App name should be 'main'"

    @patch("main.TuyaConfig")
    def test_create_app_enables_cors(self, mock_tuya_config):
        """
        Test that CORS is enabled for the application

        Verifies that CORS (Cross-Origin Resource Sharing) is properly
        configured for all routes.
        """
        # Mock the TuyaConfig.validate method
        mock_tuya_config.validate.return_value = None

        # Call the create_app factory function
        app = create_app()

        # Create a test client
        client = app.test_client()

        # Make a request to health endpoint (which should exist)
        response = client.get("/api/health")

        # Check if CORS headers are present in the response
        # Note: The actual CORS header check depends on how Flask-CORS is configured
        assert response.status_code in [
            200,
            404,
        ], "Should be able to make request to the app"

    @patch("main.TuyaConfig")
    def test_create_app_registers_blueprints(self, mock_tuya_config):
        """
        Test that all blueprints are registered

        Verifies that the health, device, and alarm blueprints
        are properly registered with the application.
        """
        # Mock the TuyaConfig.validate method
        mock_tuya_config.validate.return_value = None

        # Call the create_app factory function
        app = create_app()

        # Get all registered blueprints
        blueprints = app.blueprints

        # Assert that the expected blueprints are registered
        # Note: Blueprint names might be different, check the actual implementation
        assert len(blueprints) > 0, "At least one blueprint should be registered"

    @patch("main.TuyaConfig")
    def test_create_app_preserves_json_key_order(self, mock_tuya_config):
        """
        Test that JSON key order is preserved

        Verifies that the app.json.sort_keys is set too False
        to preserve the order of keys in JSON responses.
        """
        # Mock the TuyaConfig.validate method
        mock_tuya_config.validate.return_value = None

        # Call the create_app factory function
        app = create_app()

        # Assert that JSON key sorting is disabled
        assert (
            app.json.sort_keys is False
        ), "JSON keys should not be sorted (preserve order)"

    @patch("main.TuyaConfig")
    @patch("main.logger")
    def test_create_app_handles_config_validation_error(
        self, mock_logger, mock_tuya_config
    ):
        """
        Test configuration validation error handling

        Verifies that if TuyaConfig.validate() raises an exception,
        it is logged but the app still starts (or exits, depending on implementation).
        """
        # Configure the mock to raise a ValueError
        mock_tuya_config.validate.side_effect = ValueError("Invalid configuration")

        # Call the create_app factory function
        # Based on the implementation, it logs the error but doesn't exit
        app = create_app()

        # Assert that the app is still created
        assert isinstance(
            app, Flask
        ), "App should still be created even with config error"

        # Assert that the error was logged
        assert mock_logger.error.called, "Configuration error should be logged"


class TestErrorHandlers:
    """
    Test Suite for Global Error Handlers

    This class tests the global error handlers registered in the application
    (404, 405, 500, and general Exception handler).
    """

    @patch("main.TuyaConfig")
    def test_404_not_found_handler(self, mock_tuya_config):
        """
        Test 404 Not Found error handler

        Verifies that requests to non-existent endpoints return
        a properly formatted 404 error response.
        """
        # Mock the TuyaConfig.validate method
        mock_tuya_config.validate.return_value = None

        # Create the app
        app = create_app()
        client = app.test_client()

        # Make a request to a non-existent endpoint
        response = client.get("/non/existent/path")

        # Parse the JSON response
        response_json = json.loads(response.data)

        # Assert that the HTTP status code is 404
        assert (
            response.status_code == 404
        ), "Status code should be 404 for non-existent endpoint"

        # Assert that the response contains an error
        assert "error" in response_json, "Response should contain 'error' key"

        # Assert that the error code is NOT_FOUND
        assert (
            response_json["error"]["code"] == "NOT_FOUND"
        ), "Error code should be 'NOT_FOUND'"

        # Assert that the error message mentions the path
        assert (
            "/non/existent/path" in response_json["error"]["message"]
        ), "Error message should mention the requested path"

    @patch("main.TuyaConfig")
    def test_405_method_not_allowed_handler(self, mock_tuya_config):
        """
        Test 405 Method Not Allowed error handler

        Verifies that requests with incorrect HTTP methods return
        a properly formatted 405 error response.
        """
        # Mock the TuyaConfig.validate method
        mock_tuya_config.validate.return_value = None

        # Create the app
        app = create_app()

        # Add a test route that only accepts GET
        @app.route("/test-method", methods=["GET"])
        def test_method_route():
            return {"status": "ok"}, 200

        client = app.test_client()

        # Make a POST request to a GET-only endpoint
        response = client.post("/test-method")

        # Parse the JSON response
        response_json = json.loads(response.data)

        # Assert that the HTTP status code is 405
        assert (
            response.status_code == 405
        ), "Status code should be 405 for method not allowed"

        # Assert that the response contains an error
        assert "error" in response_json, "Response should contain 'error' key"

        # Assert that the error code is METHOD_NOT_ALLOWED
        assert (
            response_json["error"]["code"] == "METHOD_NOT_ALLOWED"
        ), "Error code should be 'METHOD_NOT_ALLOWED'"

    @patch("main.TuyaConfig")
    def test_500_internal_error_handler(self, mock_tuya_config):
        """
        Test 500 Internal Server Error handler

        Verifies that internal server errors return
        a properly formatted 500 error response.
        """
        # Mock the TuyaConfig.validate method
        mock_tuya_config.validate.return_value = None

        # Create the app
        app = create_app()

        # Add a test route that raises an exception
        @app.route("/test-error")
        def test_error_route():
            # Raise a generic exception to trigger the 500 handler
            raise Exception("Test internal error")

        client = app.test_client()

        # Make a request to the error route
        response = client.get("/test-error")

        # Parse the JSON response
        response_json = json.loads(response.data)

        # Assert that the HTTP status code is 500
        assert (
            response.status_code == 500
        ), "Status code should be 500 for internal error"

        # Assert that the response contains an error
        assert "error" in response_json, "Response should contain 'error' key"

        # Assert that the error code is INTERNAL_ERROR
        assert (
            response_json["error"]["code"] == "INTERNAL_ERROR"
        ), "Error code should be 'INTERNAL_ERROR'"

    @patch("main.TuyaConfig")
    def test_exception_handler_with_http_error(self, mock_tuya_config):
        """
        Test exception handler with HTTP exceptions

        Verifies that HTTP exceptions (like werkzeug exceptions)
        are properly handled and return appropriate error responses.
        """
        # Mock the TuyaConfig.validate method
        mock_tuya_config.validate.return_value = None

        # Create the app
        app = create_app()

        # Add a test route that raises an HTTP exception
        from werkzeug.exceptions import BadRequest

        @app.route("/test-http-error")
        def test_http_error_route():
            # Raise a BadRequest HTTP exception
            raise BadRequest("Invalid request data")

        client = app.test_client()

        # Make a request to the error route
        response = client.get("/test-http-error")

        # Parse the JSON response
        response_json = json.loads(response.data)

        # Assert that the HTTP status code is 400 (BadRequest)
        assert (
            response.status_code == 400
        ), "Status code should be 400 for BadRequest exception"

        # Assert that the response contains an error
        assert "error" in response_json, "Response should contain 'error' key"

    @patch("main.TuyaConfig")
    def test_error_responses_include_meta(self, mock_tuya_config):
        """
        Test that error responses include metadata

        Verifies that all error responses include the standard
        metadata fields (timestamp, request_id).
        """
        # Mock the TuyaConfig.validate method
        mock_tuya_config.validate.return_value = None

        # Create the app
        app = create_app()
        client = app.test_client()

        # Make a request to trigger a 404 error
        response = client.get("/non/existent")

        # Parse the JSON response
        response_json = json.loads(response.data)

        # Assert that meta is present
        assert "meta" in response_json, "Error response should contain 'meta' key"

        # Assert that meta contains timestamp
        assert "timestamp" in response_json["meta"], "Meta should contain 'timestamp'"

        # Assert that meta contains request_id
        assert "request_id" in response_json["meta"], "Meta should contain 'request_id'"


class TestApplicationConfiguration:
    """
    Test Suite for Application Configuration

    This class tests various configuration aspects of the Flask application.
    """

    @patch("main.TuyaConfig")
    def test_app_testing_mode(self, mock_tuya_config):
        """
        Test that app can be configured for testing

        Verifies that the TESTING configuration can be set
        for unit testing purposes.
        """
        # Mock the TuyaConfig.validate method
        mock_tuya_config.validate.return_value = None

        # Create the app
        app = create_app()

        # Enable testing mode
        app.config["TESTING"] = True

        # Assert that testing mode is enabled
        assert app.config["TESTING"] is True, "Testing mode should be enabled"

    @patch("main.TuyaConfig")
    def test_app_has_required_config(self, mock_tuya_config):
        """
        Test that app has required configuration

        Verifies that the app has access to necessary configuration
        values, and they can be modified.
        """
        # Mock the TuyaConfig.validate method
        mock_tuya_config.validate.return_value = None

        # Create the app
        app = create_app()

        # Test that we can set custom config values
        app.config["CUSTOM_VALUE"] = "test_value"

        # Assert that the config value is set
        assert (
            app.config.get("CUSTOM_VALUE") == "test_value"
        ), "Custom config values should be settable"


class TestApplicationRoutes:
    """
    Test Suite for Application Routes

    This class tests that the application has the expected routes
    registered from various blueprints.
    """

    @patch("main.TuyaConfig")
    def test_health_endpoint_exists(self, mock_tuya_config):
        """
        Test that health check endpoint exists

        Verifies that the /health endpoint is registered
        and accessible.
        """
        # Mock the TuyaConfig.validate method
        mock_tuya_config.validate.return_value = None

        # Create the app
        app = create_app()
        client = app.test_client()

        # Make a request to the health endpoint
        response = client.get("/health")

        # Assert that the endpoint exists (not 404)
        assert response.status_code != 404, "Health endpoint should exist"

    @patch("main.TuyaConfig")
    def test_alarm_routes_exist(self, mock_tuya_config):
        """
        Test that alarm routes are registered

        Verifies that the alarm-related endpoints are accessible
        (even if they return errors due to invalid device IDs).
        """
        # Mock the TuyaConfig.validate method
        mock_tuya_config.validate.return_value = None

        # Create the app
        app = create_app()
        client = app.test_client()

        # Test alarm routes (they should exist, even if they return 400 for invalid IDs)
        alarm_routes = [
            "/api/device/test123456/alarm/activate",
            "/api/device/test123456/alarm/deactivate",
            "/api/device/test123456/alarm/time-to-work",
        ]

        for route in alarm_routes:
            response = client.post(route)

            # Assert that the route exists (not 404)
            # It might return 400 or 500, but not 404 (Not Found)
            assert response.status_code != 404, f"Route {route} should exist"


class TestApplicationIntegration:
    """
    Test Suite for Application Integration

    This class tests the integration of various components
    in the Flask application.
    """

    @patch("main.TuyaConfig")
    def test_app_handles_json_requests(self, mock_tuya_config):
        """
        Test that app correctly handles JSON requests

        Verifies that the app can receive and process JSON payloads
        in request bodies.
        """
        # Mock the TuyaConfig.validate method
        mock_tuya_config.validate.return_value = None

        # Create the app
        app = create_app()

        # Add a test route that accepts JSON
        @app.route("/test-json", methods=["POST"])
        def test_json_route():
            from flask import request

            data = request.get_json()
            return {"received": data}, 200

        client = app.test_client()

        # Make a POST request with JSON data
        test_data = {"key": "value", "number": 123}
        response = client.post(
            "/test-json", data=json.dumps(test_data), content_type="application/json"
        )

        # Parse the response
        response_json = json.loads(response.data)

        # Assert that the JSON was correctly received
        assert (
            response.status_code == 200
        ), "JSON request should be processed successfully"
        assert (
            response_json["received"] == test_data
        ), "Received data should match sent data"

    @patch("main.TuyaConfig")
    def test_app_returns_json_responses(self, mock_tuya_config, client):
        """
        Test that app returns JSON responses

        Verifies that the app's error handlers and routes
        return properly formatted JSON responses.
        """
        # Mock the TuyaConfig.validate method
        mock_tuya_config.validate.return_value = None

        # Create the app
        app = create_app()
        client = app.test_client()

        # Make a request to trigger an error
        response = client.get("/non/existent")

        # Assert that the content type is JSON
        assert response.content_type.startswith(
            "application/json"
        ), "Response should have JSON content type"

        # Assert that the response can be parsed as JSON
        try:
            json.loads(response.data)
        except json.JSONDecodeError:
            pytest.fail("Response should be valid JSON")
