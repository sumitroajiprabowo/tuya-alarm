
import pytest
from unittest.mock import MagicMock, patch

def test_health_check(client):
    """Test the simple health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["data"]["status"] == "healthy"
    assert data["data"]["service"] == "tuya-alarm-api"

@patch("routes.health.tuya_client")
def test_credentials_check_connected(mock_tuya_client, client):
    """Test credentials check when connected."""
    mock_tuya_client.get_access_token.return_value = "fake_token"
    
    response = client.get("/credentials")
    assert response.status_code == 200
    data = response.get_json()
    assert data["data"]["tuya_api"] == "connected"
    assert data["data"]["data_center"] == "Singapore"

@patch("routes.health.tuya_client")
def test_credentials_check_disconnected(mock_tuya_client, client):
    """Test credentials check when disconnected (no token)."""
    mock_tuya_client.get_access_token.return_value = None
    
    response = client.get("/credentials")
    assert response.status_code == 200
    data = response.get_json()
    assert data["data"]["tuya_api"] == "disconnected"

@patch("routes.health.tuya_client")
def test_credentials_check_error(mock_tuya_client, client):
    """Test credentials check when detailed error occurs."""
    mock_tuya_client.get_access_token.side_effect = Exception("Connection failed")
    
    response = client.get("/credentials")
    assert response.status_code == 200
    data = response.get_json()
    assert data["data"]["tuya_api"] == "error"

def test_index_route(client):
    """Test the index route to ensure it lists new endpoints."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.get_json()
    endpoints = data["data"]["endpoints"]
    assert "health" in endpoints
    assert "credentials" in endpoints
    assert endpoints["health"] == "/health"
    assert endpoints["credentials"] == "/credentials"
