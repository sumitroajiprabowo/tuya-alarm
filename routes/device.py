"""
Device management routes
"""

from flask import Blueprint, request

from services import TuyaClient
from utils import handle_errors, validate_device_id, success_response, error_response
from constants import VolumeLevel, BrightnessLevel, MasterMode, CommandCode

# Create a Flask Blueprint named 'device' with a URL prefix for all routes
device_bp = Blueprint("device", __name__, url_prefix="/api")
# Initialize the TuyaClient instance to be used by the routes
tuya_client = TuyaClient()


# Define a route to get a list of all devices
# This route accepts GET requests at /api/devices
@device_bp.route("/devices", methods=["GET"])
# Apply the error handling decorator to catch exceptions and return standard error responses
@handle_errors
def get_devices():
    """Get list of all devices"""
    # Retrieve the list of devices from the Tuya client
    result = tuya_client.get_devices()
    # Check if the operation was not successful
    if not result.get("success"):
        # Return a standardized error response with details from the result
        return error_response(
            # Use the message from the result or a default error message
            message=result.get("msg", "Unknown error from Tuya"),
            # Use the error code from the result or a default code
            code=str(result.get("code", "TUYA_ERROR")),
            # Set the HTTP status code to 400 Bad Request
            status=400,
            # Include the full result in the details for debugging
            details=result,
        )
    # Return a standardized success response with the result data
    return success_response(result)


# Define a route to get detailed information for a specific device
# This route accepts GET requests at /api/device/<device_id>
@device_bp.route("/device/<device_id>", methods=["GET"])
# Apply the error handling decorator to catch exceptions and return standard error responses
@handle_errors
# Apply the device ID validation decorator to ensure the ID is valid
@validate_device_id
def get_device_info(device_id):
    """Get detailed device information"""
    # Retrieve the device information from the Tuya client
    result = tuya_client.get_device_info(device_id)
    # Check if the operation was not successful
    if not result.get("success"):
        # Return a standardized error response with details from the result
        return error_response(
            # Use the message from the result or a default error message
            message=result.get("msg", "Unknown error from Tuya"),
            # Use the error code from the result or a default code
            code=str(result.get("code", "TUYA_ERROR")),
            # Set the HTTP status code to 400 Bad Request
            status=400,
            # Include the full result in the details for debugging
            details=result,
        )
    # Return a standardized success response with the result data
    return success_response(result)


# Define a route to get the status of a specific device with formatted output
# This route accepts GET requests at /api/device/<device_id>/status
@device_bp.route("/device/<device_id>/status", methods=["GET"])
# Apply the error handling decorator to catch exceptions and return standard error responses
@handle_errors
# Apply the device ID validation decorator to ensure the ID is valid
@validate_device_id
def get_device_status(device_id):
    """Get device status with formatted output"""
    # Retrieve the device information (including status) from the Tuya client
    result = tuya_client.get_device_info(device_id)

    # If the operation was successful, process the status data
    if result.get("success"):
        # Extract the status list from the result
        status_data = result.get("result", {}).get("status", [])
        # Format the status list into a dictionary for easier access
        formatted_status = {item["code"]: item["value"] for item in status_data}

        # Define a list of read-only fields that might be present in the status
        readonly_fields = [
            CommandCode.BATTERY_PERCENTAGE,
            CommandCode.BATTERY_VALUE,
            CommandCode.BATTERY_STATE,
            CommandCode.CHARGE_STATE,
            CommandCode.CHECKING_RESULT,
            CommandCode.PREHEAT,
            CommandCode.LIFECYCLE,
            CommandCode.TEMPER_ALARM,
        ]

        # Iterate through read-only fields (placeholder loop for potential future logic)
        for field in readonly_fields:
            if field in formatted_status:
                # Ensure boolean fields are actual booleans if needed,
                # though Tuya usually returns them correctly.
                pass

        # Add the formatted status dictionary to the result
        result["formatted_status"] = formatted_status

    # Check if the operation was not successful
    if not result.get("success"):
        # Return a standardized error response with details from the result
        return error_response(
            # Use the message from the result or a default error message
            message=result.get("msg", "Unknown error from Tuya"),
            # Use the error code from the result or a default code
            code=str(result.get("code", "TUYA_ERROR")),
            # Set the HTTP status code to 400 Bad Request
            status=400,
            # Include the full result in the details for debugging
            details=result,
        )

    # Return a standardized success response with the result data
    return success_response(result)


# Define a route to send custom commands to a device
# This route accepts POST requests at /api/device/<device_id>/commands
@device_bp.route("/device/<device_id>/commands", methods=["POST"])
# Apply the error handling decorator to catch exceptions and return standard error responses
@handle_errors
# Apply the device ID validation decorator to ensure the ID is valid
@validate_device_id
def send_commands(device_id):
    """Send commands to device"""
    # Get the JSON data from the request body
    data = request.get_json()

    # Validate that the request body contains 'commands'
    if not data or "commands" not in data:
        return error_response(
            message="Missing commands in request body",
            code="INVALID_REQUEST",
            status=400,
        )

    # Extract the commands list
    commands = data["commands"]

    # Validate that 'commands' is a non-empty list
    if not isinstance(commands, list) or len(commands) == 0:
        return error_response(
            message="Commands must be a non-empty array",
            code="INVALID_REQUEST",
            status=400,
        )

    # Send the commands to the Tuya device using the client
    result = tuya_client.send_commands(device_id, commands)
    # Check if the command execution was not successful
    if not result.get("success"):
        # Return a standardized error response with details from the result
        return error_response(
            # Use the message from the result or a default error message
            message=result.get("msg", "Unknown error from Tuya"),
            # Use the error code from the result or a default code
            code=str(result.get("code", "TUYA_ERROR")),
            # Set the HTTP status code to 400 Bad Request
            status=400,
            # Include the full result in the details for debugging
            details=result,
        )
    # Return a standardized success response with the result data
    return success_response(result)


# Define a route to set the alarm volume for a device
# This route accepts POST requests at /api/device/<device_id>/volume/<level>
@device_bp.route("/device/<device_id>/volume/<level>", methods=["POST"])
# Apply the error handling decorator to catch exceptions and return standard error responses
@handle_errors
# Apply the device ID validation decorator to ensure the ID is valid
@validate_device_id
def set_volume(device_id, level):
    """Set alarm volume"""
    # Get all valid volume levels
    valid_levels = VolumeLevel.all()

    # Validate that the requested level is valid
    if level not in valid_levels:
        return error_response(
            message=f'Invalid volume level. Must be one of: {", ".join(valid_levels)}',
            code="INVALID_PARAM",
            status=400,
        )

    # Create the command to set the volume
    commands = [{"code": CommandCode.ALARM_VOLUME, "value": level}]
    # Send the command to the Tuya device
    result = tuya_client.send_commands(device_id, commands)
    # Check if the command execution was not successful
    if not result.get("success"):
        # Return a standardized error response with details from the result
        return error_response(
            # Use the message from the result or a default error message
            message=result.get("msg", "Unknown error from Tuya"),
            # Use the error code from the result or a default code
            code=str(result.get("code", "TUYA_ERROR")),
            # Set the HTTP status code to 400 Bad Request
            status=400,
            # Include the full result in the details for debugging
            details=result,
        )
    # Return a standardized success response with the result data
    return success_response(result)


# Define a route to set the brightness level for a device
# This route accepts POST requests at /api/device/<device_id>/brightness/<level>
@device_bp.route("/device/<device_id>/brightness/<level>", methods=["POST"])
# Apply the error handling decorator to catch exceptions and return standard error responses
@handle_errors
# Apply the device ID validation decorator to ensure the ID is valid
@validate_device_id
def set_brightness(device_id, level):
    """Set brightness level"""
    # Get all valid brightness levels
    valid_levels = BrightnessLevel.all()

    # Validate that the requested level is valid
    if level not in valid_levels:
        return error_response(
            message=f'Invalid brightness level. Must be one of: {", ".join(valid_levels)}',
            code="INVALID_PARAM",
            status=400,
        )

    # Create the command to set the brightness
    commands = [{"code": CommandCode.BRIGHT_STATE, "value": level}]
    # Send the command to the Tuya device
    result = tuya_client.send_commands(device_id, commands)
    # Check if the command execution was not successful
    if not result.get("success"):
        # Return a standardized error response with details from the result
        return error_response(
            # Use the message from the result or a default error message
            message=result.get("msg", "Unknown error from Tuya"),
            # Use the error code from the result or a default code
            code=str(result.get("code", "TUYA_ERROR")),
            # Set the HTTP status code to 400 Bad Request
            status=400,
            # Include the full result in the details for debugging
            details=result,
        )
    # Return a standardized success response with the result data
    return success_response(result)


# Define a route to set the master mode for a device
# This route accepts POST requests at /api/device/<device_id>/mode/<mode>
@device_bp.route("/device/<device_id>/mode/<mode>", methods=["POST"])
# Apply the error handling decorator to catch exceptions and return standard error responses
@handle_errors
# Apply the device ID validation decorator to ensure the ID is valid
@validate_device_id
def set_mode(device_id, mode):
    """Set master mode"""
    # Get all valid master modes
    valid_modes = MasterMode.all()

    # Validate that the requested mode is valid
    if mode not in valid_modes:
        return error_response(
            message=f'Invalid mode. Must be one of: {", ".join(valid_modes)}',
            code="INVALID_PARAM",
            status=400,
        )

    # Create the command to set the master mode
    commands = [{"code": CommandCode.MASTER_MODE, "value": mode}]

    # If setting to arm mode, also enable alert state and alarm switch
    if mode == MasterMode.ARM:
        commands.append({"code": CommandCode.ALERT_STATE, "value": True})
        commands.append({"code": CommandCode.ALARM_SWITCH, "value": True})

    # If setting to disarmed, disable alert state
    elif mode == MasterMode.DISARMED:
        commands.append({"code": CommandCode.ALERT_STATE, "value": False})

    # Send the commands to the Tuya device
    result = tuya_client.send_commands(device_id, commands)
    # Check if the command execution was not successful
    if not result.get("success"):
        # Return a standardized error response with details from the result
        return error_response(
            # Use the message from the result or a default error message
            message=result.get("msg", "Unknown error from Tuya"),
            # Use the error code from the result or a default code
            code=str(result.get("code", "TUYA_ERROR")),
            # Set the HTTP status code to 400 Bad Request
            status=400,
            # Include the full result in the details for debugging
            details=result,
        )
    # Return a standardized success response with the result data
    return success_response(result)


# Define a route to set the alarm duration for a device
# This route accepts POST requests at /api/device/<device_id>/duration/<seconds>
@device_bp.route("/device/<device_id>/duration/<int:seconds>", methods=["POST"])
# Apply the error handling decorator to catch exceptions and return standard error responses
@handle_errors
# Apply the device ID validation decorator to ensure the ID is valid
@validate_device_id
def set_duration(device_id, seconds):
    """Set alarm duration"""
    # Validate that the duration is within the allowed range (1-60 seconds)
    if seconds < 1 or seconds > 60:
        return error_response(
            message="Duration must be between 1 and 60 seconds",
            code="INVALID_PARAM",
            status=400,
        )

    # Create the command to set the alarm duration
    commands = [{"code": CommandCode.ALARM_TIME, "value": seconds}]
    # Send the command to the Tuya device
    result = tuya_client.send_commands(device_id, commands)
    # Check if the command execution was not successful
    if not result.get("success"):
        # Return a standardized error response with details from the result
        return error_response(
            # Use the message from the result or a default error message
            message=result.get("msg", "Unknown error from Tuya"),
            # Use the error code from the result or a default code
            code=str(result.get("code", "TUYA_ERROR")),
            # Set the HTTP status code to 400 Bad Request
            status=400,
            # Include the full result in the details for debugging
            details=result,
        )
    # Return a standardized success response with the result data
    return success_response(result)
