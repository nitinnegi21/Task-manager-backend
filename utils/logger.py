# utils/logger.py - Logging configuration
import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger(app):
    """
    Setup application logging
    
    Args:
        app: Flask application instance
    """
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Get log level from config
    log_level = getattr(logging, app.config['LOG_LEVEL'].upper(), logging.INFO)
    
    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format=app.config['LOG_FORMAT']
    )
    
    # File handler with rotation
    file_handler = RotatingFileHandler(
        f"logs/{app.config['LOG_FILE']}",
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(logging.Formatter(app.config['LOG_FORMAT']))
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(logging.Formatter(app.config['LOG_FORMAT']))
    
    # Add handlers to app logger
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    app.logger.setLevel(log_level)
    
    # Log startup message
    app.logger.info("="*50)
    app.logger.info("Task Management Application Starting")
    app.logger.info(f"Log Level: {app.config['LOG_LEVEL']}")
    app.logger.info("="*50)