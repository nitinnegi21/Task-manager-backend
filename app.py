from flask import Flask
from flask_cors import CORS
from config import Config
from database import init_db
from routes.task_routes import task_bp
from utils.error_handlers import register_error_handlers
from utils.logger import setup_logger
import logging

def create_app(config_class=Config):
    """
    Application factory pattern for creating Flask app
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Setup logger
    setup_logger(app)
    app.logger.info("Starting Task Management Application")
    
    # Initialize CORS
    CORS(app)
    
    # Initialize database
    init_db(app)
    
    # Register blueprints
    app.register_blueprint(task_bp, url_prefix='/api')
    
    # Register error handlers
    register_error_handlers(app)
    
    app.logger.info("Application initialized successfully")
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(
        debug=app.config['DEBUG'],
        host=app.config['HOST'],
        port=app.config['PORT']
    )