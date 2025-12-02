# Unit Tests Documentation

This directory contains comprehensive unit tests for the Tuya Alarm Control API. All tests are written with detailed English comments to ensure readability and maintainability for other developers.

## Test Structure

```
tests/
├── __init__.py                 # Test package initialization
├── conftest.py                 # Pytest configuration and shared fixtures
├── test_response.py            # Tests for utils/response.py
├── test_decorators.py          # Tests for utils/decorators.py
├── test_tuya_client.py         # Tests for services/tuya_client.py
├── test_alarm_routes.py        # Tests for routes/alarm.py
├── test_main.py                # Tests for main.py (Flask app factory)
└── README.md                   # This file
```

## Prerequisites

Before running the tests, ensure you have installed the testing dependencies:

```bash
# Install all dependencies including testing packages
pip install -r requirements.txt
```

## Running Tests

### Run All Tests

To run all unit tests in the project:

```bash
# Run from the project root directory
pytest

# Or with verbose output
pytest -v

# Or with very verbose output showing each test
pytest -vv
```

### Run Specific Test Files

To run tests for a specific module:

```bash
# Test response utilities
pytest tests/test_response.py

# Test decorators
pytest tests/test_decorators.py

# Test Tuya client
pytest tests/test_tuya_client.py

# Test alarm routes
pytest tests/test_alarm_routes.py

# Test main application
pytest tests/test_main.py
```

### Run Specific Test Classes or Methods

To run a specific test class or method:

```bash
# Run a specific test class
pytest tests/test_response.py::TestSuccessResponse

# Run a specific test method
pytest tests/test_response.py::TestSuccessResponse::test_success_response_with_data_only
```

### Run Tests with Coverage

To see test coverage (what percentage of code is tested):

```bash
# Generate coverage report
pytest --cov=. --cov-report=html

# View the coverage report in your browser
# Open htmlcov/index.html in a web browser

# Or get a terminal-based coverage report
pytest --cov=. --cov-report=term-missing
```

### Run Tests with Specific Markers

If tests are marked with pytest markers (e.g., @pytest.mark.slow):

```bash
# Run only slow tests
pytest -m slow

# Run everything except slow tests
pytest -m "not slow"
```

## Test Files Overview

### 1. test_response.py
Tests the standardized API response formatting functions.

**What it tests:**
- `success_response()` function with various data types
- `error_response()` function with different error codes and status codes
- Response format consistency (data, meta, timestamp, request_id)
- Edge cases (None data, empty lists, custom metadata)

**Key test classes:**
- `TestSuccessResponse` - Tests for successful API responses
- `TestErrorResponse` - Tests for error API responses

### 2. test_decorators.py
Tests the Flask route decorators used for error handling and validation.

**What it tests:**
- `@handle_errors` decorator catching exceptions
- `@validate_device_id` decorator validating device IDs
- Combined usage of multiple decorators
- Function metadata preservation (@wraps functionality)

**Key test classes:**
- `TestHandleErrorsDecorator` - Tests error handling decorator
- `TestValidateDeviceIdDecorator` - Tests device ID validation
- `TestDecoratorsCombined` - Tests multiple decorators together

### 3. test_tuya_client.py
Tests the TuyaClient service that communicates with the Tuya API.

**What it tests:**
- SHA256 and HMAC-SHA256 hashing functions
- Signature building for API authentication
- Access token retrieval and caching
- HTTP request methods (GET, POST, PUT, DELETE)
- Device management methods (get_devices, get_device_info, send_commands)
- Error handling for network failures and API errors

**Key test classes:**
- `TestTuyaClientHashingMethods` - Tests cryptographic functions
- `TestTuyaClientSignatureBuilding` - Tests signature generation
- `TestTuyaClientGetAccessToken` - Tests token management
- `TestTuyaClientRequest` - Tests API request methods
- `TestTuyaClientDeviceMethods` - Tests high-level device methods

### 4. test_alarm_routes.py
Tests the alarm control API endpoints.

**What it tests:**
- Emergency alarm activation endpoint
- Alarm deactivation endpoint
- Time-to-work alarm endpoint
- Preset application endpoint
- Request validation (device ID validation)
- Error handling and response formatting
- Integration with TuyaClient

**Key test classes:**
- `TestActivateAlarmRoute` - Tests emergency alarm activation
- `TestDeactivateAlarmRoute` - Tests alarm deactivation
- `TestTimeToWorkAlarmRoute` - Tests time-to-work alarm
- `TestApplyPresetRoute` - Tests preset application
- `TestAlarmRoutesIntegration` - Tests route integration aspects

### 5. test_main.py
Tests the Flask application factory and global configuration.

**What it tests:**
- `create_app()` factory function
- Blueprint registration
- CORS configuration
- Global error handlers (404, 405, 500, Exception)
- JSON configuration
- Application integration

**Key test classes:**
- `TestCreateApp` - Tests application factory
- `TestErrorHandlers` - Tests global error handlers
- `TestApplicationConfiguration` - Tests app configuration
- `TestApplicationRoutes` - Tests route registration
- `TestApplicationIntegration` - Tests component integration

## Writing New Tests

When writing new tests, follow these guidelines:

### 1. File Naming Convention
- Test files should start with `test_` prefix
- Name should match the module being tested: `test_<module_name>.py`

### 2. Class Naming Convention
- Test classes should start with `Test` prefix
- Use descriptive names: `TestFunctionNameOrFeature`
- Include a docstring explaining what the class tests

### 3. Method Naming Convention
- Test methods should start with `test_` prefix
- Use descriptive names: `test_function_does_something_specific`
- Include a docstring explaining what the test verifies

### 4. Comment Every Line
- Add comments explaining what each line does
- Use clear, simple English
- Explain the "why" not just the "what"
- Help other developers understand the test logic

### Example Test Structure

```python
class TestExampleFunction:
    """
    Test Suite for example_function

    This class tests the example_function that does something specific.
    """

    def test_example_with_valid_input(self):
        """
        Test example_function with valid input

        Verifies that when valid input is provided, the function
        returns the expected output without errors.
        """
        # Define test input data
        test_input = "valid_data"

        # Call the function being tested
        result = example_function(test_input)

        # Assert that the result is correct
        assert result == "expected_output", "Function should return expected output"

        # Assert additional conditions
        assert result is not None, "Result should not be None"
```

## Mocking External Dependencies

The tests use `unittest.mock` to mock external dependencies:

### Common Mocking Patterns

```python
# Mock a function
@patch('module.function_name')
def test_something(mock_function):
    mock_function.return_value = "mocked_value"
    # Test code here

# Mock a class method
@patch.object(ClassName, 'method_name')
def test_something(mock_method):
    mock_method.return_value = "mocked_value"
    # Test code here

# Mock an API call
@patch('requests.get')
def test_something(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {'key': 'value'}
    mock_get.return_value = mock_response
    # Test code here
```

## Test Fixtures

Shared test fixtures are defined in `conftest.py`:

- `app` - Flask application instance configured for testing
- `client` - Flask test client for making HTTP requests
- `runner` - Flask CLI test runner

### Using Fixtures

```python
def test_something(client):
    """Test that uses the client fixture"""
    # The client fixture is automatically injected by pytest
    response = client.get('/api/health')
    assert response.status_code == 200
```

## Continuous Integration

These tests are designed to run in CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run tests
  run: |
    pip install -r requirements.txt
    pytest --cov=. --cov-report=xml
```

## Troubleshooting

### Import Errors

If you encounter import errors:

```bash
# Ensure you're in the project root directory
cd /path/to/tuya-alarm

# Set PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Run tests
pytest
```

### Mock Not Working

If mocks are not being applied:

- Check the patch path - it should be where the object is used, not where it's defined
- Ensure the patch decorator is above other decorators
- Verify the mock is configured before the test code runs

### Test Failures

If tests fail unexpectedly:

```bash
# Run with verbose output to see details
pytest -vv

# Run with print statements visible
pytest -s

# Run with detailed failure information
pytest -vv --tb=long
```

## Coverage Goals

Aim for high test coverage:

- **80%+** overall code coverage
- **90%+** for critical business logic (TuyaClient, alarm routes)
- **100%** for utility functions (response, decorators)

## Best Practices

1. **Test Isolation**: Each test should be independent and not rely on other tests
2. **Clear Assertions**: Use descriptive assertion messages
3. **Mock External Calls**: Always mock network requests, database calls, etc.
4. **Test Edge Cases**: Include tests for error conditions and edge cases
5. **Readable Tests**: Write tests that serve as documentation
6. **Fast Tests**: Keep tests fast by mocking slow operations
7. **Maintainable Tests**: Update tests when code changes

## Contributing

When adding new features:

1. Write tests first (Test-Driven Development)
2. Ensure all tests pass before committing
3. Add comments explaining complex test logic
4. Update this README if adding new test patterns

## Contact

For questions about the tests, please contact the development team or create an issue in the project repository.