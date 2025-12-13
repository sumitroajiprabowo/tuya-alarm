"""
Standardized API Response Helpers
"""

# Import uuid for generating request IDs
import uuid

# Import datetime for timestamps
from datetime import datetime

# Import jsonify for creating JSON responses
from flask import jsonify


def success_response(data=None, meta=None):
    """
    Format success response

    Args:
        data: Response data payload
        meta: Optional metadata dict

    Returns:
        JSON response tuple (json, status_code)
    """
    # Initialize meta if not provided
    if meta is None:
        meta = {}

    # Add standard meta fields (timestamp and request_id)
    meta.update(
        {"timestamp": datetime.now().isoformat(), "request_id": str(uuid.uuid4())}
    )

    # Construct the response dictionary
    response = {"data": data if data is not None else {}, "meta": meta}

    # Return the JSON response with status code 200
    return jsonify(response), 200


def error_response(message, code="INTERNAL_ERROR", status=500, details=None):
    """
    Format error response

    Args:
        message: Error message
        code: Error code string
        status: HTTP status code
        details: Optional error details

    Returns:
        JSON response tuple (json, status_code)
    """
    # Construct the response dictionary with error details and metadata
    response = {
        "error": {
            "code": code,
            "message": message,
            "status": status,
            "details": details if details is not None else {},
        },
        "meta": {
            "timestamp": datetime.now().isoformat(),
            "request_id": str(uuid.uuid4()),
        },
    }

    # Return the JSON response with the specified status code
    return jsonify(response), status
