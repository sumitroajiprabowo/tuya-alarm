"""
Decorators for Flask routes
"""
# Import logging module
import logging
# Import wraps to preserve function metadata
from functools import wraps
# Import datetime (though unused in this file, kept for potential future use)
from datetime import datetime
# Import jsonify (unused here as error_response handles it, but kept if needed)
from flask import jsonify
# Import error_response helper
from .response import error_response

# Get logger instance
logger = logging.getLogger(__name__)


def handle_errors(f):
    """Decorator to handle errors and return JSON response"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            # Execute the decorated function
            return f(*args, **kwargs)
        except Exception as e:
            # Log the error with the function name
            logger.error(f"Error in {f.__name__}: {str(e)}")
            # Return a standardized error response
            return error_response(
                message=str(e),
                code='INTERNAL_ERROR',
                status=500
            )
    return decorated_function


def validate_device_id(f):
    """Decorator to validate device_id parameter"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Retrieve device_id from kwargs
        device_id = kwargs.get('device_id')
        # Check if device_id is missing or too short
        if not device_id or len(device_id) < 10:
            # Return an error response for invalid device ID
            return error_response(
                message='Invalid device_id',
                code='INVALID_PARAM',
                status=400
            )
        # Proceed with the original function if validation passes
        return f(*args, **kwargs)
    return decorated_function