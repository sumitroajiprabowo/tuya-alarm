import logging
import warnings
from flask import Flask
from flask_cors import CORS

from config import FlaskConfig, TuyaConfig
from routes.device import device_bp
from routes.alarm import alarm_bp
from routes.health import health_bp

# Suppress OpenSSL warnings that might clutter the logs
warnings.filterwarnings('ignore', message='.*OpenSSL.*')

# Setup application logging configuration
logging.basicConfig(
    level=getattr(logging, FlaskConfig.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
# Get the logger instance for the main module
logger = logging.getLogger(__name__)


def create_app():
    """Create and configure Flask application"""
    # Initialize the Flask application
    app = Flask(__name__)
    app.json.sort_keys = False  # Preserve JSON key order in responses
    CORS(app)  # Enable Cross-Origin Resource Sharing (CORS) for all routes

    # Validate Tuya configuration settings
    try:
        TuyaConfig.validate()
    except ValueError as e:
        # Log an error if configuration is invalid
        logger.error(f"Configuration Error: {e}")
        # We might want to exit here, or just log the error
        # sys.exit(1)

    # Register the blueprints for different parts of the application
    app.register_blueprint(health_bp)
    app.register_blueprint(device_bp)
    app.register_blueprint(alarm_bp)

    # Global Error Handlers
    from flask import request
    from utils.response import error_response

    # Handle 404 Not Found errors
    @app.errorhandler(404)
    def not_found_error(error):
        return error_response(
            message=f"Endpoint {request.path} not found",
            code="NOT_FOUND",
            status=404
        )

    # Handle 405 Method Not Allowed errors
    @app.errorhandler(405)
    def method_not_allowed_error(error):
        return error_response(
            message="Method not allowed",
            code="METHOD_NOT_ALLOWED",
            status=405
        )

    # Handle 500 Internal Server Error
    @app.errorhandler(500)
    def internal_error(error):
        return error_response(
            message="Internal server error",
            code="INTERNAL_ERROR",
            status=500
        )
    
    # Handle generic Exceptions
    @app.errorhandler(Exception)
    def handle_exception(e):
        # Pass through HTTP errors if they have a code attribute
        if hasattr(e, 'code'):
            return error_response(
                message=str(e),
                code="HTTP_ERROR",
                status=e.code
            )
        
        # Handle non-HTTP exceptions as Internal Server Errors
        return error_response(
            message=str(e),
            code="INTERNAL_ERROR",
            status=500
        )

    return app


if __name__ == '__main__':
    # Create the application instance
    app = create_app()

    # Log startup information
    logger.info("=" * 60)
    logger.info("Tuya Alarm Control API")
    logger.info(f"Data Center: Singapore")
    logger.info("=" * 60)
    logger.info(f"Server starting on http://{FlaskConfig.HOST}:{FlaskConfig.PORT}")
    logger.info(f"Debug mode: {FlaskConfig.DEBUG}")
    logger.info("=" * 60)

    # Run the Flask application
    app.run(
        host=FlaskConfig.HOST,
        port=FlaskConfig.PORT,
        debug=FlaskConfig.DEBUG
    )
