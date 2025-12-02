"""
Tuya API Configuration - Singapore Data Center
"""
import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class TuyaConfig:
    """Tuya API Configuration - Singapore"""

    # API Credentials
    ACCESS_ID = os.getenv('TUYA_ACCESS_ID')
    ACCESS_SECRET = os.getenv('TUYA_ACCESS_SECRET')
    ENDPOINT = os.getenv('TUYA_ENDPOINT', 'https://openapi-sg.iotbing.com')

    # Token cache
    token_cache = {
        'token': None,
        'expire_time': 0
    }

    @classmethod
    def validate(cls):
        """Validate required environment variables"""
        if not cls.ACCESS_ID:
            raise ValueError("TUYA_ACCESS_ID environment variable is required")
        if not cls.ACCESS_SECRET:
            raise ValueError("TUYA_ACCESS_SECRET environment variable is required")
        if not cls.ENDPOINT:
            raise ValueError("TUYA_ENDPOINT environment variable is required")

        logger.info("Configuration loaded from environment")
        logger.info(f"   Access ID: {cls.ACCESS_ID[:10]}...")
        logger.info(f"   Endpoint: {cls.ENDPOINT}")


class FlaskConfig:
    """Flask Application Configuration"""
    HOST = os.getenv('FLASK_HOST', '0.0.0.0')
    PORT = int(os.getenv('FLASK_PORT', 5000))
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')