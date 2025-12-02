"""Routes module"""
from .health import health_bp
from .device import device_bp
from .alarm import alarm_bp

__all__ = ['health_bp', 'device_bp', 'alarm_bp']