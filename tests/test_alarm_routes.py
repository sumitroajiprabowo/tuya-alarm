"""
Unit Tests for Alarm Routes (routes/alarm.py)
This module tests the alarm control endpoints and their integration with TuyaClient
"""

# Import json module for JSON operations
import json

# Import Mock and patch for mocking dependencies
from unittest.mock import patch


class TestActivateAlarmRoute:
    """
    Test Suite for Activate Emergency Alarm Route

    This class tests the POST /api/device/<device_id>/alarm/activate endpoint
    that activates the emergency alarm for a device.
    """

    @patch("routes.alarm.tuya_client")
    def test_activate_alarm_success(self, mock_tuya_client, client):
        """
        Test successful emergency alarm activation

        Verifies that a valid request to activate the emergency alarm
        returns a success response.
        """
        # Configure the mock TuyaClient to return success
        mock_tuya_client.send_commands.return_value = {
            "success": True,
            "result": {"code": "success"},
        }

        # Define a valid device ID (10+ characters)
        device_id = "device123456"

        # Make a POST request to activate alarm
        response = client.post(f"/api/device/{device_id}/alarm/activate")

        # Parse the JSON response
        response_json = json.loads(response.data)

        # Assert that the HTTP status code is 200
        assert (
            response.status_code == 200
        ), "Status code should be 200 for successful activation"

        # Assert that the response contains data
        assert "data" in response_json, "Response should contain 'data' key"

        # Assert that send_commands was called on the TuyaClient
        assert (
            mock_tuya_client.send_commands.called
        ), "TuyaClient.send_commands should be called"

        # Verify the send_commands was called with correct device_id
        call_args = mock_tuya_client.send_commands.call_args
        assert (
            call_args[0][0] == device_id
        ), "send_commands should be called with correct device_id"

    @patch("routes.alarm.tuya_client")
    def test_activate_alarm_with_invalid_device_id(self, mock_tuya_client, client):
        """
        Test alarm activation with invalid device ID

        Verifies that a request with a short/invalid device ID
        returns a 400 error response.
        """
        # Define an invalid device ID (less than 10 characters)
        invalid_device_id = "short123"

        # Make a POST request with invalid device ID
        response = client.post(f"/api/device/{invalid_device_id}/alarm/activate")

        # Parse the JSON response
        response_json = json.loads(response.data)

        # Assert that the HTTP status code is 400
        assert (
            response.status_code == 400
        ), "Status code should be 400 for invalid device_id"

        # Assert that the response contains an error
        assert "error" in response_json, "Response should contain 'error' key"

        # Assert that the error code is INVALID_PARAM
        assert (
            response_json["error"]["code"] == "INVALID_PARAM"
        ), "Error code should be 'INVALID_PARAM'"

        # Assert that send_commands was NOT called
        assert (
            not mock_tuya_client.send_commands.called
        ), "send_commands should not be called for invalid device_id"

    @patch("routes.alarm.tuya_client")
    def test_activate_alarm_tuya_api_failure(self, mock_tuya_client, client):
        """
        Test alarm activation when Tuya API returns error

        Verifies that when the Tuya API returns a failure response,
        the route returns an appropriate error response.
        """
        # Configure the mock TuyaClient to return failure
        mock_tuya_client.send_commands.return_value = {
            "success": False,
            "msg": "Device offline",
            "code": 1001,
        }

        # Define a valid device ID
        device_id = "device123456"

        # Make a POST request to activate alarm
        response = client.post(f"/api/device/{device_id}/alarm/activate")

        # Parse the JSON response
        response_json = json.loads(response.data)

        # Assert that the HTTP status code is 400
        assert (
            response.status_code == 400
        ), "Status code should be 400 for Tuya API failure"

        # Assert that the response contains an error
        assert "error" in response_json, "Response should contain 'error' key"

        # Assert that the error message contains Tuya's error message
        assert (
            "Device offline" in response_json["error"]["message"]
        ), "Error message should contain Tuya's error message"

    @patch("routes.alarm.tuya_client")
    def test_activate_alarm_exception_handling(self, mock_tuya_client, client):
        """
        Test alarm activation with exception

        Verifies that exceptions raised during alarm activation
        are caught and returned as error responses.
        """
        # Configure the mock TuyaClient to raise an exception
        mock_tuya_client.send_commands.side_effect = Exception("Connection failed")

        # Define a valid device ID
        device_id = "device123456"

        # Make a POST request to activate alarm
        response = client.post(f"/api/device/{device_id}/alarm/activate")

        # Parse the JSON response
        response_json = json.loads(response.data)

        # Assert that the HTTP status code is 500
        assert response.status_code == 500, "Status code should be 500 for exception"

        # Assert that the response contains an error
        assert "error" in response_json, "Response should contain 'error' key"


class TestDeactivateAlarmRoute:
    """
    Test Suite for Deactivate Alarm Route

    This class tests the POST /api/device/<device_id>/alarm/deactivate endpoint
    that deactivates the alarm for a device.
    """

    @patch("routes.alarm.tuya_client")
    def test_deactivate_alarm_success(self, mock_tuya_client, client):
        """
        Test successful alarm deactivation

        Verifies that a valid request to deactivate the alarm
        returns a success response.
        """
        # Configure the mock TuyaClient to return success
        mock_tuya_client.send_commands.return_value = {
            "success": True,
            "result": {"code": "success"},
        }

        # Define a valid device ID
        device_id = "device123456"

        # Make a POST request to deactivate alarm
        response = client.post(f"/api/device/{device_id}/alarm/deactivate")

        # Parse the JSON response
        response_json = json.loads(response.data)

        # Assert that the HTTP status code is 200
        assert (
            response.status_code == 200
        ), "Status code should be 200 for successful deactivation"

        # Assert that the response contains data
        assert "data" in response_json, "Response should contain 'data' key"

        # Assert that send_commands was called
        assert (
            mock_tuya_client.send_commands.called
        ), "TuyaClient.send_commands should be called"

    @patch("routes.alarm.tuya_client")
    def test_deactivate_alarm_with_invalid_device_id(self, mock_tuya_client, client):
        """
        Test alarm deactivation with invalid device ID

        Verifies that a request with an invalid device ID
        returns a 400 error response.
        """
        # Define an invalid device ID
        invalid_device_id = "short"

        # Make a POST request with invalid device ID
        response = client.post(f"/api/device/{invalid_device_id}/alarm/deactivate")

        # Parse the JSON response
        response_json = json.loads(response.data)

        # Assert that the HTTP status code is 400
        assert (
            response.status_code == 400
        ), "Status code should be 400 for invalid device_id"

        # Assert that the response contains an error
        assert "error" in response_json, "Response should contain 'error' key"

        # Assert that send_commands was NOT called
        assert (
            not mock_tuya_client.send_commands.called
        ), "send_commands should not be called for invalid device_id"


class TestTimeToWorkAlarmRoute:
    """
    Test Suite for Time to Work Alarm Route

    This class tests the POST /api/device/<device_id>/alarm/time-to-work endpoint
    that activates the time-to-work alarm.
    """

    @patch("routes.alarm.tuya_client")
    def test_time_to_work_alarm_success(self, mock_tuya_client, client):
        """
        Test successful time-to-work alarm activation

        Verifies that a valid request to activate the time-to-work alarm
        returns a success response.
        """
        # Configure the mock TuyaClient to return success
        mock_tuya_client.send_commands.return_value = {
            "success": True,
            "result": {"code": "success"},
        }

        # Define a valid device ID
        device_id = "device123456"

        # Make a POST request to activate time-to-work alarm
        response = client.post(f"/api/device/{device_id}/alarm/time-to-work")

        # Parse the JSON response
        response_json = json.loads(response.data)

        # Assert that the HTTP status code is 200
        assert (
            response.status_code == 200
        ), "Status code should be 200 for successful activation"

        # Assert that the response contains data
        assert "data" in response_json, "Response should contain 'data' key"

        # Assert that send_commands was called
        assert (
            mock_tuya_client.send_commands.called
        ), "TuyaClient.send_commands should be called"

    @patch("routes.alarm.tuya_client")
    def test_time_to_work_alarm_tuya_failure(self, mock_tuya_client, client):
        """
        Test time-to-work alarm when Tuya API fails

        Verifies that Tuya API failures are properly handled
        and returned as error responses.
        """
        # Configure the mock TuyaClient to return failure
        mock_tuya_client.send_commands.return_value = {
            "success": False,
            "msg": "Command failed",
            "code": 2001,
        }

        # Define a valid device ID
        device_id = "device123456"

        # Make a POST request
        response = client.post(f"/api/device/{device_id}/alarm/time-to-work")

        # Parse the JSON response
        response_json = json.loads(response.data)

        # Assert that the HTTP status code is 400
        assert response.status_code == 400, "Status code should be 400 for Tuya failure"

        # Assert that the response contains an error
        assert "error" in response_json, "Response should contain 'error' key"


class TestApplyPresetRoute:
    """
    Test Suite for Apply Preset Route

    This class tests the POST /api/device/<device_id>/preset/<preset_name> endpoint
    that applies predefined alarm presets to devices.
    """

    @patch(
        "routes.alarm.ALARM_PRESETS",
        {
            "morning": [{"code": "alarm_volume", "value": 50}],
            "night": [{"code": "alarm_volume", "value": 20}],
        },
    )
    @patch("routes.alarm.tuya_client")
    def test_apply_preset_success(self, mock_tuya_client, client):
        """
        Test successful preset application

        Verifies that a valid preset can be applied to a device
        and returns a success response.
        """
        # Configure the mock TuyaClient to return success
        mock_tuya_client.send_commands.return_value = {
            "success": True,
            "result": {"code": "success"},
        }

        # Define a valid device ID and preset name
        device_id = "device123456"
        preset_name = "morning"

        # Make a POST request to apply preset
        response = client.post(f"/api/device/{device_id}/preset/{preset_name}")

        # Parse the JSON response
        response_json = json.loads(response.data)

        # Assert that the HTTP status code is 200
        assert (
            response.status_code == 200
        ), "Status code should be 200 for successful preset application"

        # Assert that the response contains data
        assert "data" in response_json, "Response should contain 'data' key"

        # Assert that send_commands was called
        assert (
            mock_tuya_client.send_commands.called
        ), "TuyaClient.send_commands should be called"

    @patch(
        "routes.alarm.ALARM_PRESETS",
        {
            "morning": [{"code": "alarm_volume", "value": 50}],
            "night": [{"code": "alarm_volume", "value": 20}],
        },
    )
    @patch("routes.alarm.tuya_client")
    def test_apply_preset_invalid_preset_name(self, mock_tuya_client, client):
        """
        Test preset application with invalid preset name

        Verifies that requesting an invalid/non-existent preset
        returns a 400 error with available preset names.
        """
        # Define a valid device ID but invalid preset name
        device_id = "device123456"
        invalid_preset = "invalid_preset"

        # Make a POST request with invalid preset
        response = client.post(f"/api/device/{device_id}/preset/{invalid_preset}")

        # Parse the JSON response
        response_json = json.loads(response.data)

        # Assert that the HTTP status code is 400
        assert (
            response.status_code == 400
        ), "Status code should be 400 for invalid preset"

        # Assert that the response contains an error
        assert "error" in response_json, "Response should contain 'error' key"

        # Assert that the error message mentions available presets
        assert (
            "Invalid preset" in response_json["error"]["message"]
        ), "Error message should indicate invalid preset"

        # Assert that the error code is INVALID_PARAM
        assert (
            response_json["error"]["code"] == "INVALID_PARAM"
        ), "Error code should be 'INVALID_PARAM'"

        # Assert that send_commands was NOT called
        assert (
            not mock_tuya_client.send_commands.called
        ), "send_commands should not be called for invalid preset"

    @patch(
        "routes.alarm.ALARM_PRESETS",
        {"morning": [{"code": "alarm_volume", "value": 50}]},
    )
    @patch("routes.alarm.tuya_client")
    def test_apply_preset_with_invalid_device_id(self, mock_tuya_client, client):
        """
        Test preset application with invalid device ID

        Verifies that even with a valid preset, an invalid device ID
        returns a 400 error.
        """
        # Define an invalid device ID
        invalid_device_id = "short"
        preset_name = "morning"

        # Make a POST request with invalid device ID
        response = client.post(f"/api/device/{invalid_device_id}/preset/{preset_name}")

        # Parse the JSON response
        response_json = json.loads(response.data)

        # Assert that the HTTP status code is 400
        assert (
            response.status_code == 400
        ), "Status code should be 400 for invalid device_id"

        # Assert that the response contains an error
        assert "error" in response_json, "Response should contain 'error' key"

        # Assert that send_commands was NOT called
        assert (
            not mock_tuya_client.send_commands.called
        ), "send_commands should not be called for invalid device_id"

    @patch(
        "routes.alarm.ALARM_PRESETS",
        {
            "morning": [{"code": "alarm_volume", "value": 50}],
            "night": [{"code": "alarm_volume", "value": 20}],
            "emergency": [{"code": "alarm_volume", "value": 100}],
        },
    )
    @patch("routes.alarm.tuya_client")
    def test_apply_preset_multiple_presets(self, mock_tuya_client, client):
        """
        Test applying different presets

        Verifies that different presets can be applied and that
        the correct preset commands are sent to the TuyaClient.
        """
        # Configure the mock TuyaClient to return success
        mock_tuya_client.send_commands.return_value = {
            "success": True,
            "result": {"code": "success"},
        }

        # Define a valid device ID
        device_id = "device123456"

        # Test multiple presets
        presets = ["morning", "night", "emergency"]

        for preset_name in presets:
            # Reset the mock call count
            mock_tuya_client.send_commands.reset_mock()

            # Make a POST request to apply preset
            response = client.post(f"/api/device/{device_id}/preset/{preset_name}")

            # Assert that the HTTP status code is 200
            assert (
                response.status_code == 200
            ), f"Status code should be 200 for preset '{preset_name}'"

            # Assert that send_commands was called
            assert (
                mock_tuya_client.send_commands.called
            ), f"send_commands should be called for preset '{preset_name}'"


class TestAlarmRoutesIntegration:
    """
    Test Suite for Alarm Routes Integration

    This class tests the integration aspects of the alarm routes,
    including error handling, logging, and response formatting.
    """

    @patch("routes.alarm.tuya_client")
    @patch("routes.alarm.logger")
    def test_alarm_routes_logging(self, mock_logger, mock_tuya_client, client):
        """
        Test that alarm routes properly log actions

        Verifies that important actions (activate, deactivate) are logged
        with appropriate log levels (info, warning).
        """
        # Configure the mock TuyaClient to return success
        mock_tuya_client.send_commands.return_value = {
            "success": True,
            "result": {"code": "success"},
        }

        # Define a valid device ID
        device_id = "device123456"

        # Test activate alarm (should log warning)
        client.post(f"/api/device/{device_id}/alarm/activate")
        # Assert that warning was logged for emergency activation
        assert (
            mock_logger.warning.called
        ), "Warning should be logged for emergency alarm activation"

        # Reset the mock
        mock_logger.reset_mock()

        # Test deactivate alarm (should log info)
        client.post(f"/api/device/{device_id}/alarm/deactivate")
        # Assert that info was logged for deactivation
        assert mock_logger.info.called, "Info should be logged for alarm deactivation"

    @patch("routes.alarm.tuya_client")
    def test_alarm_routes_response_format(self, mock_tuya_client, client):
        """
        Test response format consistency

        Verifies that all alarm routes return responses in the
        standardized format (with data/meta for success, error/meta for failures).
        """
        # Configure the mock TuyaClient to return success
        mock_tuya_client.send_commands.return_value = {
            "success": True,
            "result": {"code": "success"},
        }

        # Define a valid device ID
        device_id = "device123456"

        # Test each alarm route
        routes = [
            f"/api/device/{device_id}/alarm/activate",
            f"/api/device/{device_id}/alarm/deactivate",
            f"/api/device/{device_id}/alarm/time-to-work",
        ]

        for route_path in routes:
            # Make a POST request
            response = client.post(route_path)

            # Parse the JSON response
            response_json = json.loads(response.data)

            # Assert that response has standard structure
            assert (
                "data" in response_json
            ), f"Success response for {route_path} should contain 'data'"
            assert (
                "meta" in response_json
            ), f"Success response for {route_path} should contain 'meta'"
            assert (
                "timestamp" in response_json["meta"]
            ), f"Meta should contain 'timestamp' for {route_path}"
            assert (
                "request_id" in response_json["meta"]
            ), f"Meta should contain 'request_id' for {route_path}"
