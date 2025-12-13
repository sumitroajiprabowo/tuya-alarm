"""
Pytest Configuration and Shared Fixtures
This file contains common test fixtures used across multiple test modules
"""

# Import pytest framework for test configuration and fixtures
import pytest

# Import sys and os for path manipulation
import sys
import os

# Add the parent directory to the Python path
# This allows importing modules from the project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import the Flask app factory function from main module
from main import create_app


@pytest.fixture
def app():
    """
    Flask Application Fixture

    Creates a Flask application instance configured for testing.
    This fixture is used by other fixtures and tests that need the app context.

    Returns:
        Flask: A Flask application instance with testing configuration
    """
    # Create the Flask application using the factory function
    app = create_app()

    # Enable testing mode which disables error catching during request handling
    # This allows exceptions to propagate and be caught by the test framework
    app.config["TESTING"] = True

    # Disable CSRF protection during testing to simplify test requests
    app.config["WTF_CSRF_ENABLED"] = False

    # Return the configured app instance
    return app


@pytest.fixture
def client(app):
    """
    Flask Test Client Fixture

    Creates a test client for making requests to the application.
    This client simulates HTTP requests without running a real server.

    Args:
        app: Flask application fixture (automatically injected by pytest)

    Returns:
        FlaskClient: A test client for making HTTP requests to the app
    """
    # Create and return a test client from the Flask application
    # This client can be used to make GET, POST, PUT, DELETE requests
    return app.test_client()


@pytest.fixture
def runner(app):
    """
    Flask CLI Runner Fixture

    Creates a test runner for CLI commands.
    Useful for testing command-line interface commands.

    Args:
        app: Flask application fixture (automatically injected by pytest)

    Returns:
        FlaskCliRunner: A test runner for CLI commands
    """
    # Create and return a CLI test runner from the Flask application
    return app.test_cli_runner()
