"""
Health and info routes
"""
# Import Blueprint for route organization from Flask
from flask import Blueprint
# Import the TuyaClient service to interact with Tuya devices
from services import TuyaClient
# Import TuyaConfig to access configuration settings
from config import TuyaConfig

# Import success_response helper for standardized responses
from utils import success_response

# Create a Flask Blueprint named 'health'
health_bp = Blueprint('health', __name__)
# Initialize the TuyaClient instance
tuya_client = TuyaClient()


# Define the index route
# This route accepts GET requests at /
@health_bp.route('/')
def index():
    """API welcome page"""
    # Define the data to be returned in the response
    data = {
        'name': 'Tuya Alarm Control API',
        'version': '2.0.0',
        'data_center': 'Singapore',
        'status': 'running',
        'endpoints': {
            'health': '/health',
            'devices': '/api/devices',
            'device_info': '/api/device/<device_id>',
            'device_status': '/api/device/<device_id>/status',
            'send_commands': '/api/device/<device_id>/commands',
            'activate_alarm': '/api/device/<device_id>/alarm/activate',
            'deactivate_alarm': '/api/device/<device_id>/alarm/deactivate',
            'set_volume': '/api/device/<device_id>/volume/<level>',
            'set_brightness': '/api/device/<device_id>/brightness/<level>',
            'set_mode': '/api/device/<device_id>/mode/<mode>',
            'set_duration': '/api/device/<device_id>/duration/<seconds>',
            'apply_preset': '/api/device/<device_id>/preset/<preset_name>'
        }
    }
    # Return a standardized success response with the data
    return success_response(data)


# Define the health check route
# This route accepts GET requests at /health
@health_bp.route('/health')
def health_check():
    """Health check endpoint"""
    try:
        # Attempt to get an access token to verify Tuya API connectivity
        token = tuya_client.get_access_token()
        # Set api_status based on whether a token was retrieved
        api_status = 'connected' if token else 'disconnected'
    except:
        # If an exception occurs, set api_status to 'error'
        api_status = 'error'

    # Define the health status data
    data = {
        'status': 'healthy',
        'tuya_api': api_status,
        'data_center': 'Singapore',
        'endpoint': TuyaConfig.ENDPOINT
    }
    # Return a standardized success response with the health data
    return success_response(data)