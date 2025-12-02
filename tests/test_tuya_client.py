"""
Unit Tests for Tuya Client Service (services/tuya_client.py)
This module tests the TuyaClient class that handles Tuya API communication
"""
# Import pytest framework for testing
import pytest
# Import Mock and patch for mocking external dependencies
from unittest.mock import Mock, patch
# Import the TuyaClient class to be tested
from services.tuya_client import TuyaClient


class TestTuyaClientHashingMethods:
    """
    Test Suite for TuyaClient Hashing Methods

    This class tests the cryptographic hashing methods used for
    signature generation in the Tuya API authentication.
    """

    def test_sha256_hash_with_string(self):
        """
        Test SHA256 hashing with string input

        Verifies that the _sha256_hash method correctly hashes
        a string input and returns the expected hexadecimal digest.
        """
        # Create an instance of TuyaClient
        client = TuyaClient()

        # Define a test string
        test_string = "test_data"

        # Call the _sha256_hash method
        result = client._sha256_hash(test_string)

        # Assert that the result is a string
        assert isinstance(result, str), "Hash result should be a string"

        # Assert that the result has the correct length (SHA256 produces 64 hex characters)
        assert len(result) == 64, "SHA256 hash should be 64 characters long"

        # Assert that the result matches the expected hash
        # This is the known SHA256 hash of "test_data"
        expected_hash = "e7d87b738825c33824cf3fd32b7314161fc8c425129163ff5e7260fc7288da36"
        assert result == expected_hash, "Hash should match expected value"

    def test_sha256_hash_with_bytes(self):
        """
        Test SHA256 hashing with bytes input

        Verifies that the _sha256_hash method correctly handles
        bytes input (not just strings).
        """
        # Create an instance of TuyaClient
        client = TuyaClient()

        # Define test data as bytes
        test_bytes = b"test_data"

        # Call the _sha256_hash method with bytes
        result = client._sha256_hash(test_bytes)

        # Assert that the result is a string
        assert isinstance(result, str), "Hash result should be a string"

        # Assert that the result has the correct length
        assert len(result) == 64, "SHA256 hash should be 64 characters long"

        # The hash should be the same as hashing "test_data" as string
        expected_hash = "e7d87b738825c33824cf3fd32b7314161fc8c425129163ff5e7260fc7288da36"
        assert result == expected_hash, "Hash of bytes should match hash of equivalent string"

    def test_sha256_hash_with_none(self):
        """
        Test SHA256 hashing with None input

        Verifies that the _sha256_hash method handles None input
        by treating it as empty data.
        """
        # Create an instance of TuyaClient
        client = TuyaClient()

        # Call the _sha256_hash method with None
        result = client._sha256_hash(None)

        # Assert that the result is a string
        assert isinstance(result, str), "Hash result should be a string"

        # Assert that the result matches the hash of empty data
        # This is the known SHA256 hash of empty string
        expected_hash = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        assert result == expected_hash, "Hash of None should match hash of empty data"

    def test_sha256_hash_with_empty_string(self):
        """
        Test SHA256 hashing with empty string

        Verifies that the _sha256_hash method correctly hashes
        an empty string.
        """
        # Create an instance of TuyaClient
        client = TuyaClient()

        # Call the _sha256_hash method with empty string
        result = client._sha256_hash("")

        # Expected hash of empty string
        expected_hash = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        assert result == expected_hash, "Hash of empty string should match expected value"

    def test_hmac_sha256(self):
        """
        Test HMAC-SHA256 signing

        Verifies that the _hmac_sha256 method correctly generates
        HMAC signatures using SHA256.
        """
        # Create an instance of TuyaClient
        client = TuyaClient()

        # Define test message and secret key
        message = "test_message"
        secret = "test_secret"

        # Call the _hmac_sha256 method
        result = client._hmac_sha256(message, secret)

        # Assert that the result is a string
        assert isinstance(result, str), "HMAC result should be a string"

        # Assert that the result is in uppercase (as per implementation)
        assert result.isupper(), "HMAC result should be uppercase"

        # Assert that the result has the correct length (64 hex characters)
        assert len(result) == 64, "HMAC-SHA256 should be 64 characters long"

        # Verify the result is deterministic (same inputs produce same output)
        result2 = client._hmac_sha256(message, secret)
        assert result == result2, "HMAC should be deterministic"

    def test_hmac_sha256_with_different_secrets(self):
        """
        Test HMAC-SHA256 with different secret keys

        Verifies that different secret keys produce different signatures
        for the same message.
        """
        # Create an instance of TuyaClient
        client = TuyaClient()

        # Define test message and two different secrets
        message = "test_message"
        secret1 = "secret_key_1"
        secret2 = "secret_key_2"

        # Generate HMAC with first secret
        result1 = client._hmac_sha256(message, secret1)

        # Generate HMAC with second secret
        result2 = client._hmac_sha256(message, secret2)

        # Assert that the two HMACs are different
        assert result1 != result2, "Different secrets should produce different HMACs"


class TestTuyaClientSignatureBuilding:
    """
    Test Suite for TuyaClient Signature Building

    This class tests the _build_signature method that creates
    authentication signatures for Tuya API requests.
    """

    @patch('services.tuya_client.TuyaConfig')
    def test_build_signature_basic(self, mock_config):
        """
        Test basic signature building

        Verifies that the _build_signature method correctly constructs
        a signature string using the provided parameters.
        """
        # Configure the mock config with test credentials
        mock_config.ACCESS_ID = "test_access_id"
        mock_config.ACCESS_SECRET = "test_secret"

        # Create an instance of TuyaClient
        client = TuyaClient()
        # Set the client's config to use the mock
        client.config = mock_config

        # Define test parameters
        method = "GET"
        path = "/v1.0/devices"
        body = ""
        timestamp = "1234567890"
        token = ""

        # Call the _build_signature method
        result = client._build_signature(method, path, body, timestamp, token)

        # Assert that the result is a string
        assert isinstance(result, str), "Signature should be a string"

        # Assert that the result is uppercase (HMAC is uppercase)
        assert result.isupper(), "Signature should be uppercase"

        # Assert that the result has the correct length (64 hex characters)
        assert len(result) == 64, "Signature should be 64 characters long"

    @patch('services.tuya_client.TuyaConfig')
    def test_build_signature_with_body(self, mock_config):
        """
        Test signature building with request body

        Verifies that the signature correctly includes the request body
        (used for POST/PUT requests).
        """
        # Configure the mock config
        mock_config.ACCESS_ID = "test_access_id"
        mock_config.ACCESS_SECRET = "test_secret"

        # Create an instance of TuyaClient
        client = TuyaClient()
        client.config = mock_config

        # Define test parameters with a body
        method = "POST"
        path = "/v1.0/devices/123/commands"
        body = '{"commands":[{"code":"switch","value":true}]}'
        timestamp = "1234567890"
        token = "test_token"

        # Call the _build_signature method
        result = client._build_signature(method, path, body, timestamp, token)

        # Assert that the result is a valid signature
        assert isinstance(result, str), "Signature should be a string"
        assert len(result) == 64, "Signature should be 64 characters long"

        # Verify that a different body produces a different signature
        different_body = '{"commands":[{"code":"switch","value":false}]}'
        different_result = client._build_signature(method, path, different_body, timestamp, token)
        assert result != different_result, "Different bodies should produce different signatures"

    @patch('services.tuya_client.TuyaConfig')
    def test_build_signature_with_token(self, mock_config):
        """
        Test signature building with access token

        Verifies that the signature correctly includes the access token
        (used for authenticated API requests).
        """
        # Configure the mock config
        mock_config.ACCESS_ID = "test_access_id"
        mock_config.ACCESS_SECRET = "test_secret"

        # Create an instance of TuyaClient
        client = TuyaClient()
        client.config = mock_config

        # Build signature without token
        result_without_token = client._build_signature(
            "GET", "/v1.0/devices", "", "1234567890", ""
        )

        # Build signature with token
        result_with_token = client._build_signature(
            "GET", "/v1.0/devices", "", "1234567890", "test_token_123"
        )

        # Assert that token affects the signature
        assert result_without_token != result_with_token, \
            "Token should change the signature"


class TestTuyaClientGetAccessToken:
    """
    Test Suite for TuyaClient Get Access Token

    This class tests the get_access_token method that retrieves
    and caches access tokens from the Tuya API.
    """

    @patch('services.tuya_client.requests.get')
    @patch('services.tuya_client.TuyaConfig')
    @patch('services.tuya_client.time.time')
    def test_get_access_token_success(self, mock_time, mock_config, mock_requests):
        """
        Test successful access token retrieval

        Verifies that the get_access_token method correctly requests
        and caches a new access token.
        """
        # Mock the current time
        mock_time.return_value = 1000.0  # 1000 seconds (1000000 milliseconds)

        # Configure the mock config
        mock_config.ACCESS_ID = "test_access_id"
        mock_config.ACCESS_SECRET = "test_secret"
        mock_config.ENDPOINT = "https://openapi.tuyacn.com"
        # Mock empty token cache
        mock_config.token_cache = {'token': None, 'expire_time': 0}

        # Create a mock response for the token request
        mock_response = Mock()
        mock_response.json.return_value = {
            'success': True,
            'result': {
                'access_token': 'new_token_12345',
                'expire_time': 7200  # 2 hours
            }
        }
        # Configure requests.get to return the mock response
        mock_requests.return_value = mock_response

        # Create an instance of TuyaClient
        client = TuyaClient()
        client.config = mock_config

        # Call the get_access_token method
        token = client.get_access_token()

        # Assert that the returned token is correct
        assert token == 'new_token_12345', "Should return the new access token"

        # Assert that requests.get was called
        assert mock_requests.called, "requests.get should be called"

        # Assert that the token was cached
        assert mock_config.token_cache['token'] == 'new_token_12345', \
            "Token should be cached"

    @patch('services.tuya_client.requests.get')
    @patch('services.tuya_client.TuyaConfig')
    @patch('services.tuya_client.time.time')
    def test_get_access_token_uses_cache(self, mock_time, mock_config, mock_requests):
        """
        Test that cached token is used when valid

        Verifies that if a valid cached token exists, it is returned
        without making a new API request.
        """
        # Mock the current time
        current_time = 1000000.0  # 1000000000 milliseconds
        mock_time.return_value = current_time

        # Configure the mock config with a valid cached token
        mock_config.ACCESS_ID = "test_access_id"
        mock_config.ACCESS_SECRET = "test_secret"
        mock_config.ENDPOINT = "https://openapi.tuyacn.com"
        # Set a cached token that hasn't expired
        mock_config.token_cache = {
            'token': 'cached_token_12345',
            'expire_time': (current_time + 1000) * 1000  # Expires in future
        }

        # Create an instance of TuyaClient
        client = TuyaClient()
        client.config = mock_config

        # Call the get_access_token method
        token = client.get_access_token()

        # Assert that the cached token is returned
        assert token == 'cached_token_12345', "Should return cached token"

        # Assert that requests.get was NOT called (cache was used)
        assert not mock_requests.called, "requests.get should not be called when cache is valid"

    @patch('services.tuya_client.requests.get')
    @patch('services.tuya_client.TuyaConfig')
    @patch('services.tuya_client.time.time')
    def test_get_access_token_api_failure(self, mock_time, mock_config, mock_requests):
        """
        Test access token retrieval when API returns error

        Verifies that an exception is raised when the Tuya API
        returns a failure response.
        """
        # Mock the current time
        mock_time.return_value = 1000.0

        # Configure the mock config
        mock_config.ACCESS_ID = "test_access_id"
        mock_config.ACCESS_SECRET = "test_secret"
        mock_config.ENDPOINT = "https://openapi.tuyacn.com"
        mock_config.token_cache = {'token': None, 'expire_time': 0}

        # Create a mock response with failure
        mock_response = Mock()
        mock_response.json.return_value = {
            'success': False,
            'msg': 'Invalid credentials',
            'code': 1001
        }
        mock_requests.return_value = mock_response

        # Create an instance of TuyaClient
        client = TuyaClient()
        client.config = mock_config

        # Assert that an exception is raised
        with pytest.raises(Exception) as exc_info:
            client.get_access_token()

        # Assert that the exception message contains the error
        assert 'Failed to get token' in str(exc_info.value), \
            "Exception should indicate token retrieval failure"

    @patch('services.tuya_client.requests.get')
    @patch('services.tuya_client.TuyaConfig')
    @patch('services.tuya_client.time.time')
    def test_get_access_token_network_error(self, mock_time, mock_config, mock_requests):
        """
        Test access token retrieval with network error

        Verifies that network errors are properly caught and
        re-raised as exceptions with descriptive messages.
        """
        # Mock the current time
        mock_time.return_value = 1000.0

        # Configure the mock config
        mock_config.ACCESS_ID = "test_access_id"
        mock_config.ACCESS_SECRET = "test_secret"
        mock_config.ENDPOINT = "https://openapi.tuyacn.com"
        mock_config.token_cache = {'token': None, 'expire_time': 0}

        # Configure requests.get to raise a network error
        import requests
        mock_requests.side_effect = requests.exceptions.ConnectionError("Network unreachable")

        # Create an instance of TuyaClient
        client = TuyaClient()
        client.config = mock_config

        # Assert that an exception is raised
        with pytest.raises(Exception) as exc_info:
            client.get_access_token()

        # Assert that the exception message indicates network error
        assert 'Network error' in str(exc_info.value), \
            "Exception should indicate network error"


class TestTuyaClientRequest:
    """
    Test Suite for TuyaClient Request Method

    This class tests the request method that makes authenticated
    requests to the Tuya API.
    """

    @patch('services.tuya_client.requests.get')
    @patch.object(TuyaClient, 'get_access_token')
    @patch('services.tuya_client.TuyaConfig')
    def test_request_get_success(self, mock_config, mock_get_token, mock_requests):
        """
        Test successful GET request

        Verifies that a GET request is correctly constructed and executed.
        """
        # Configure mocks
        mock_config.ACCESS_ID = "test_access_id"
        mock_config.ACCESS_SECRET = "test_secret"
        mock_config.ENDPOINT = "https://openapi.tuyacn.com"

        # Mock the get_access_token method to return a test token
        mock_get_token.return_value = "test_token_12345"

        # Create a mock successful response
        mock_response = Mock()
        mock_response.json.return_value = {
            'success': True,
            'result': {'device_id': '123', 'status': 'online'}
        }
        mock_requests.return_value = mock_response

        # Create an instance of TuyaClient
        client = TuyaClient()
        client.config = mock_config

        # Make a GET request
        result = client.request('GET', '/v1.0/devices/123')

        # Assert that the result is successful
        assert result['success'] is True, "Request should be successful"
        assert 'result' in result, "Response should contain 'result'"

        # Assert that requests.get was called
        assert mock_requests.called, "requests.get should be called"

    @patch('services.tuya_client.requests.post')
    @patch.object(TuyaClient, 'get_access_token')
    @patch('services.tuya_client.TuyaConfig')
    def test_request_post_with_body(self, mock_config, mock_get_token, mock_requests):
        """
        Test successful POST request with body

        Verifies that a POST request with a JSON body is correctly
        constructed and executed.
        """
        # Configure mocks
        mock_config.ACCESS_ID = "test_access_id"
        mock_config.ACCESS_SECRET = "test_secret"
        mock_config.ENDPOINT = "https://openapi.tuyacn.com"

        mock_get_token.return_value = "test_token_12345"

        # Create a mock successful response
        mock_response = Mock()
        mock_response.json.return_value = {
            'success': True,
            'result': {'code': 'success'}
        }
        mock_requests.return_value = mock_response

        # Create an instance of TuyaClient
        client = TuyaClient()
        client.config = mock_config

        # Define request body
        body = {'commands': [{'code': 'switch', 'value': True}]}

        # Make a POST request
        result = client.request('POST', '/v1.0/devices/123/commands', body)

        # Assert that the result is successful
        assert result['success'] is True, "Request should be successful"

        # Assert that requests.post was called
        assert mock_requests.called, "requests.post should be called"

        # Get the call arguments
        call_args = mock_requests.call_args

        # Assert that the body was sent as JSON string
        assert 'data' in call_args.kwargs, "Request should include data"

    @patch('services.tuya_client.requests.get')
    @patch.object(TuyaClient, 'get_access_token')
    @patch('services.tuya_client.TuyaConfig')
    def test_request_timeout(self, mock_config, mock_get_token, mock_requests):
        """
        Test request timeout handling

        Verifies that timeout errors are properly caught and
        re-raised as exceptions.
        """
        # Configure mocks
        mock_config.ACCESS_ID = "test_access_id"
        mock_config.ACCESS_SECRET = "test_secret"
        mock_config.ENDPOINT = "https://openapi.tuyacn.com"

        mock_get_token.return_value = "test_token_12345"

        # Configure requests to raise timeout error
        import requests
        mock_requests.side_effect = requests.exceptions.Timeout("Request timed out")

        # Create an instance of TuyaClient
        client = TuyaClient()
        client.config = mock_config

        # Assert that an exception is raised for timeout
        with pytest.raises(Exception) as exc_info:
            client.request('GET', '/v1.0/devices/123')

        # Assert that the exception message indicates timeout
        assert 'timeout' in str(exc_info.value).lower(), \
            "Exception should indicate timeout"

    def test_request_unsupported_method(self):
        """
        Test request with unsupported HTTP method

        Verifies that unsupported HTTP methods raise an appropriate exception.
        """
        # Create an instance of TuyaClient
        with patch.object(TuyaClient, 'get_access_token', return_value="test_token"):
            client = TuyaClient()

            # Assert that an exception is raised for unsupported method
            with pytest.raises(Exception) as exc_info:
                client.request('PATCH', '/v1.0/devices/123')

            # Assert that the exception indicates unsupported method
            assert 'Unsupported HTTP method' in str(exc_info.value), \
                "Exception should indicate unsupported HTTP method"


class TestTuyaClientDeviceMethods:
    """
    Test Suite for TuyaClient Device Methods

    This class tests the high-level device management methods
    (get_devices, get_device_info, send_commands).
    """

    @patch.object(TuyaClient, 'request')
    def test_get_devices(self, mock_request):
        """
        Test get_devices method

        Verifies that get_devices correctly calls the request method
        with the appropriate parameters.
        """
        # Configure mock to return a successful response
        mock_request.return_value = {
            'success': True,
            'result': [{'device_id': '123'}, {'device_id': '456'}]
        }

        # Create an instance of TuyaClient
        client = TuyaClient()

        # Call get_devices
        result = client.get_devices()

        # Assert that request was called with correct parameters
        mock_request.assert_called_once_with('GET', '/v1.0/devices')

        # Assert that the result is returned
        assert result['success'] is True, "Should return successful result"

    @patch.object(TuyaClient, 'request')
    def test_get_device_info(self, mock_request):
        """
        Test get_device_info method

        Verifies that get_device_info correctly calls the request method
        with the device ID in the path.
        """
        # Configure mock to return a successful response
        mock_request.return_value = {
            'success': True,
            'result': {'device_id': 'device123', 'name': 'Test Device'}
        }

        # Create an instance of TuyaClient
        client = TuyaClient()

        # Call get_device_info
        device_id = 'device123'
        result = client.get_device_info(device_id)

        # Assert that request was called with correct parameters
        mock_request.assert_called_once_with('GET', f'/v1.0/devices/{device_id}')

        # Assert that the result is returned
        assert result['success'] is True, "Should return successful result"

    @patch.object(TuyaClient, 'request')
    def test_send_commands_success(self, mock_request):
        """
        Test send_commands method with valid commands

        Verifies that send_commands correctly sends a list of commands
        to the specified device.
        """
        # Configure mock to return a successful response
        mock_request.return_value = {
            'success': True,
            'result': {'success': True}
        }

        # Create an instance of TuyaClient
        client = TuyaClient()

        # Define test commands
        device_id = 'device123'
        commands = [
            {'code': 'switch', 'value': True},
            {'code': 'brightness', 'value': 80}
        ]

        # Call send_commands
        result = client.send_commands(device_id, commands)

        # Assert that request was called with correct parameters
        mock_request.assert_called_once_with(
            'POST',
            f'/v1.0/devices/{device_id}/commands',
            {'commands': commands}
        )

        # Assert that the result is successful
        assert result['success'] is True, "Should return successful result"

    def test_send_commands_with_empty_list(self):
        """
        Test send_commands with empty command list

        Verifies that send_commands raises an exception when
        an empty command list is provided.
        """
        # Create an instance of TuyaClient
        client = TuyaClient()

        # Assert that ValueError is raised for empty list
        with pytest.raises(ValueError) as exc_info:
            client.send_commands('device123', [])

        # Assert that the exception message is appropriate
        assert 'non-empty list' in str(exc_info.value), \
            "Exception should indicate list must be non-empty"

    def test_send_commands_with_non_list(self):
        """
        Test send_commands with non-list input

        Verifies that send_commands raises an exception when
        commands is not a list.
        """
        # Create an instance of TuyaClient
        client = TuyaClient()

        # Assert that ValueError is raised for non-list input
        with pytest.raises(ValueError) as exc_info:
            client.send_commands('device123', {'code': 'switch'})

        # Assert that the exception message is appropriate
        assert 'must be a' in str(exc_info.value).lower(), \
            "Exception should indicate commands must be a list"