"""
Tuya API Client Service
Handles all Tuya API communication and authentication
"""
# Import hashlib for SHA256 hashing
import hashlib
# Import hmac for HMAC-SHA256 signature generation
import hmac
# Import time for timestamp generation and cache management
import time
# Import json for JSON serialization
import json
# Import logging for application logging
import logging
# Import requests for making HTTP requests
import requests

# Import TuyaConfig for configuration settings
from config import TuyaConfig

# Get logger instance
logger = logging.getLogger(__name__)


class TuyaClient:
    """Tuya API Client - Singapore Data Center"""

    def __init__(self):
        # Initialize with configuration
        self.config = TuyaConfig

    @staticmethod
    def _sha256_hash(data):
        """SHA256 hash"""
        # Encode string data to bytes if necessary
        if isinstance(data, str):
            data = data.encode('utf-8')
        # Handle None input as empty bytes
        elif data is None:
            data = b''
        # Return the hexadecimal representation of the SHA256 hash
        return hashlib.sha256(data).hexdigest()

    @staticmethod
    def _hmac_sha256(message, secret):
        """HMAC-SHA256"""
        # Create a new HMAC object using the secret and message
        return hmac.new(
            secret.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        # Return the uppercase hexadecimal representation of the HMAC
        ).hexdigest().upper()

    def _build_signature(self, method, path, body, timestamp, token=""):
        """
        Build signature following Tuya Singapore format

        Args:
            method: HTTP method
            path: API path with query params
            body: Request body string
            timestamp: Timestamp
            token: Access token (empty for token request)

        Returns:
            Signature string
        """
        # 1. Calculate SHA256 hash of the content (body)
        content_sha256 = self._sha256_hash(body if body else "")

        # 2. Define headers (empty for basic requests in this implementation)
        headers = ""

        # 3. Define the URL string (path)
        url_str = path

        # 4. Construct the string to sign
        string_to_sign = f"{method}\n{content_sha256}\n{headers}\n{url_str}"

        # 5. Concatenate ID, token, timestamp, and string to sign
        sign_str = self.config.ACCESS_ID + token + timestamp + string_to_sign

        # 6. Calculate HMAC-SHA256 signature using the access secret
        sign = self._hmac_sha256(sign_str, self.config.ACCESS_SECRET)

        return sign

    def get_access_token(self):
        """
        Get Tuya access token (with caching)

        Returns:
            Access token string

        Raises:
            Exception: If token retrieval fails
        """
        # Check if cached token is still valid
        current_time = time.time() * 1000
        if (self.config.token_cache['token'] and
                current_time < self.config.token_cache['expire_time']):
            logger.info("Using cached access token")
            return self.config.token_cache['token']

        try:
            # Generate current timestamp
            timestamp = str(int(time.time() * 1000))
            method = "GET"
            path = "/v1.0/token?grant_type=1"

            # Build signature (no token required for token request)
            sign = self._build_signature(method, path, "", timestamp, "")

            # Prepare headers for the request
            headers = {
                'client_id': self.config.ACCESS_ID,
                'sign': sign,
                't': timestamp,
                'sign_method': 'HMAC-SHA256'
            }

            # Construct the full URL
            url = self.config.ENDPOINT + path
            # Make the GET request to fetch the token
            response = requests.get(url, headers=headers, timeout=10)
            data = response.json()

            # Check if the request was successful
            if data.get('success'):
                token = data['result']['access_token']
                # Calculate expiration time (subtract 60 seconds for safety buffer)
                expire_time = current_time + (data['result']['expire_time'] - 60) * 1000

                # Cache the new token and expiration time
                self.config.token_cache['token'] = token
                self.config.token_cache['expire_time'] = expire_time

                logger.info("Successfully obtained new access token")
                logger.info(f"Token expires in {data['result']['expire_time']} seconds")
                return token
            else:
                # Handle API error response
                error_msg = f"Failed to get token: {data.get('msg', 'Unknown error')}"
                logger.error(error_msg)
                logger.error(f"Full response: {data}")
                raise Exception(error_msg)

        except requests.exceptions.RequestException as e:
            # Handle network errors
            logger.error(f"Network error getting token: {str(e)}")
            raise Exception(f"Network error: {str(e)}")
        except Exception as e:
            # Handle other exceptions
            logger.error(f"Error getting access token: {str(e)}")
            raise

    def request(self, method, path, body=None):
        """
        Make authenticated request to Tuya API

        Args:
            method: HTTP method (GET, POST, etc.)
            path: API endpoint path
            body: Request body dict (for POST requests)

        Returns:
            Response JSON data

        Raises:
            Exception: If request fails
        """
        try:
            # Get a valid access token
            token = self.get_access_token()
            # Generate current timestamp
            timestamp = str(int(time.time() * 1000))

            # Build body string if body is present
            body_str = ""
            if body:
                # Use separators to ensure compact JSON representation
                body_str = json.dumps(body, separators=(',', ':'))

            # Build signature for the request
            sign = self._build_signature(method, path, body_str, timestamp, token)

            # Prepare headers including authentication details
            headers = {
                'client_id': self.config.ACCESS_ID,
                'access_token': token,
                'sign': sign,
                't': timestamp,
                'sign_method': 'HMAC-SHA256',
                'Content-Type': 'application/json'
            }

            # Construct the full URL
            url = self.config.ENDPOINT + path

            logger.info(f"Making {method} request to: {path}")

            # Execute the HTTP request based on the method
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=10)
            elif method == 'POST':
                response = requests.post(url, headers=headers, data=body_str, timeout=10)
            elif method == 'PUT':
                response = requests.put(url, headers=headers, data=body_str, timeout=10)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, timeout=10)
            else:
                raise Exception(f'Unsupported HTTP method: {method}')

            # Parse the JSON response
            result = response.json()

            # Log success or failure based on the response content
            if result.get('success'):
                logger.info(f"Request successful: {path}")
            else:
                logger.warning(f"Request failed: {result.get('msg', 'Unknown error')}")
                logger.warning(f"Full response: {result}")

            return result

        except requests.exceptions.Timeout:
            # Handle request timeout
            logger.error(f"Request timeout for: {path}")
            raise Exception("Request timeout")
        except requests.exceptions.RequestException as e:
            # Handle network errors
            logger.error(f"Network error: {str(e)}")
            raise Exception(f"Network error: {str(e)}")
        except Exception as e:
            # Handle other exceptions
            logger.error(f"Error in Tuya request: {str(e)}")
            raise

    def get_devices(self):
        """Get list of all devices"""
        # Send GET request to fetch devices
        return self.request('GET', '/v1.0/devices')

    def get_device_info(self, device_id):
        """Get detailed device information"""
        # Send GET request to fetch specific device info
        return self.request('GET', f'/v1.0/devices/{device_id}')

    def send_commands(self, device_id, commands):
        """
        Send commands to device

        Args:
            device_id: Device ID
            commands: List of command dicts

        Returns:
            Response data
        """
        # Validate that commands is a non-empty list
        if not isinstance(commands, list) or len(commands) == 0:
            raise ValueError('Commands must be a non-empty list')

        logger.info(f"Sending {len(commands)} commands to device {device_id}")

        # Send POST request to issue commands to the device
        return self.request(
            'POST',
            f'/v1.0/devices/{device_id}/commands',
            {'commands': commands}
        )