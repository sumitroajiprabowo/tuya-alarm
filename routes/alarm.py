"""
Alarm control routes
"""
# Import the logging module to handle application logging
import logging
# Import Blueprint for route organization and jsonify for JSON responses from Flask
from flask import Blueprint

# Import the TuyaClient service to interact with Tuya devices
from services import TuyaClient
# Import utility functions for error handling, validation, and standardized responses
from utils import handle_errors, validate_device_id, success_response, error_response
# Import constant values for alarm presets and command definitions
from constants import (ALARM_PRESETS, EMERGENCY_ALARM_COMMANDS, DEACTIVATE_ALARM_COMMANDS,
                       TIME_TO_WORK_COMMANDS)

# Create a Flask Blueprint named 'alarm' with a URL prefix for all routes
alarm_bp = Blueprint('alarm', __name__, url_prefix='/api/device')
# Initialize the TuyaClient instance to be used by the routes
tuya_client = TuyaClient()
# Get a logger instance for this module to log events and errors
logger = logging.getLogger(__name__)


# Define a route to activate the emergency alarm for a specific device
# This route accepts POST requests at /api/device/<device_id>/alarm/activate
@alarm_bp.route('/<device_id>/alarm/activate', methods=['POST'])
# Apply the error handling decorator to catch exceptions and return standard error responses
@handle_errors
# Apply the device ID validation decorator to ensure the ID is valid
@validate_device_id
def activate_alarm(device_id):
    """Activate emergency alarm"""
    # Log a warning message indicating that the emergency alarm is being activated
    logger.warning(f"EMERGENCY ALARM ACTIVATED for device {device_id}")
    # Send the emergency alarm commands to the Tuya device using the client
    result = tuya_client.send_commands(device_id, EMERGENCY_ALARM_COMMANDS)
    # Check if the command execution was not successful
    if not result.get('success'):
        # Return a standardized error response with details from the result
        return error_response(
            # Use the message from the result or a default error message
            message=result.get('msg', 'Unknown error from Tuya'),
            # Use the error code from the result or a default code
            code=str(result.get('code', 'TUYA_ERROR')),
            # Set the HTTP status code to 400 Bad Request
            status=400,
            # Include the full result in the details for debugging
            details=result
        )
    # Return a standardized success response with the result data
    return success_response(result)


# Define a route to deactivate the alarm for a specific device
# This route accepts POST requests at /api/device/<device_id>/alarm/deactivate
@alarm_bp.route('/<device_id>/alarm/deactivate', methods=['POST'])
# Apply the error handling decorator to catch exceptions and return standard error responses
@handle_errors
# Apply the device ID validation decorator to ensure the ID is valid
@validate_device_id
def deactivate_alarm(device_id):
    """Deactivate alarm"""
    # Log an info message indicating that the alarm is being deactivated
    logger.info(f"Alarm deactivated for device {device_id}")
    # Send the deactivate alarm commands to the Tuya device using the client
    result = tuya_client.send_commands(device_id, DEACTIVATE_ALARM_COMMANDS)
    # Check if the command execution was not successful
    if not result.get('success'):
        # Return a standardized error response with details from the result
        return error_response(
            # Use the message from the result or a default error message
            message=result.get('msg', 'Unknown error from Tuya'),
            # Use the error code from the result or a default code
            code=str(result.get('code', 'TUYA_ERROR')),
            # Set the HTTP status code to 400 Bad Request
            status=400,
            # Include the full result in the details for debugging
            details=result
        )
    # Return a standardized success response with the result data
    return success_response(result)


# Define a route to activate the 'time to work' alarm for a specific device
# This route accepts POST requests at /api/device/<device_id>/alarm/time-to-work
@alarm_bp.route('/<device_id>/alarm/time-to-work', methods=['POST'])
# Apply the error handling decorator to catch exceptions and return standard error responses
@handle_errors
# Apply the device ID validation decorator to ensure the ID is valid
@validate_device_id
def time_to_work_alarm(device_id):
    """Activate time to work alarm"""
    # Log a warning message indicating that the time-to-work alarm is being activated
    logger.warning(f"TIME TO WORK ALARM ACTIVATED for device {device_id}")
    # Send the time-to-work alarm commands to the Tuya device using the client
    result = tuya_client.send_commands(device_id, TIME_TO_WORK_COMMANDS)
    # Check if the command execution was not successful
    if not result.get('success'):
        # Return a standardized error response with details from the result
        return error_response(
            # Use the message from the result or a default error message
            message=result.get('msg', 'Unknown error from Tuya'),
            # Use the error code from the result or a default code
            code=str(result.get('code', 'TUYA_ERROR')),
            # Set the HTTP status code to 400 Bad Request
            status=400,
            # Include the full result in the details for debugging
            details=result
        )
    # Return a standardized success response with the result data
    return success_response(result)


# Define a route to apply a specific alarm preset to a device
# This route accepts POST requests at /api/device/<device_id>/preset/<preset_name>
@alarm_bp.route('/<device_id>/preset/<preset_name>', methods=['POST'])
# Apply the error handling decorator to catch exceptions and return standard error responses
@handle_errors
# Apply the device ID validation decorator to ensure the ID is valid
@validate_device_id
def apply_preset(device_id, preset_name):
    """Apply predefined preset configurations"""
    # Check if the requested preset name exists in the available presets
    if preset_name not in ALARM_PRESETS:
        # Return an error response if the preset is invalid
        return error_response(
            # Provide a message listing the available presets
            message=f'Invalid preset. Available: {", ".join(ALARM_PRESETS.keys())}',
            # Set the error code to INVALID_PARAM
            code='INVALID_PARAM',
            # Set the HTTP status code to 400 Bad Request
            status=400
        )

    # Retrieve the list of commands corresponding to the requested preset
    commands = ALARM_PRESETS[preset_name]
    # Log an info message indicating that the preset is being applied
    logger.info(f"Applying preset '{preset_name}' to device {device_id}")

    # Send the preset commands to the Tuya device using the client
    result = tuya_client.send_commands(device_id, commands)
    # Check if the command execution was not successful
    if not result.get('success'):
        # Return a standardized error response with details from the result
        return error_response(
            # Use the message from the result or a default error message
            message=result.get('msg', 'Unknown error from Tuya'),
            # Use the error code from the result or a default code
            code=str(result.get('code', 'TUYA_ERROR')),
            # Set the HTTP status code to 400 Bad Request
            status=400,
            # Include the full result in the details for debugging
            details=result
        )
    # Return a standardized success response with the result data
    return success_response(result)