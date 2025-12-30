# utils/error_handlers.py - Global error handlers
from flask import jsonify
from werkzeug.exceptions import HTTPException
import logging

logger = logging.getLogger(__name__)

def register_error_handlers(app):
    """Register error handlers for the Flask application"""
    
    @app.errorhandler(400)
    def bad_request(error):
        logger.warning(f"Bad request: {str(error)}")
        return jsonify({
            'success': False,
            'status_code': 400,
            'error': 'Bad request',
            'error_detail': str(error)
        }), 400
    
    @app.errorhandler(404)
    def not_found(error):
        logger.warning(f"Resource not found: {str(error)}")
        return jsonify({
            'success': False,
            'status_code': 404,
            'error': 'Resource not found',
            'error_detail': str(error)
        }), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        logger.warning(f"Method not allowed: {str(error)}")
        return jsonify({
            'success': False,
            'status_code': 405,
            'error': 'Method not allowed',
            'error_detail': str(error)
        }), 405
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal server error: {str(error)}")
        return jsonify({
            'success': False,
            'status_code': 500,
            'error': 'Internal server error',
            'error_detail': 'An unexpected error occurred. Please try again later.'
        }), 500
    
    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        logger.warning(f"HTTP exception: {error.code} - {error.description}")
        return jsonify({
            'success': False,
            'status_code': error.code,
            'error': error.name,
            'error_detail': error.description
        }), error.code
    
    @app.errorhandler(Exception)
    def handle_generic_exception(error):
        logger.error(f"Unhandled exception: {str(error)}", exc_info=True)
        return jsonify({
            'success': False,
            'status_code': 500,
            'error': 'Internal server error',
            'error_detail': 'An unexpected error occurred. Please try again later.'
        }), 500