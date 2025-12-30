# utils/response.py - Response helper functions
from flask import jsonify

def success_response(data=None, message=None, status_code=200):
    """
    Create a standardized success response
    
    Args:
        data: Response data
        message: Success message
        status_code: HTTP status code
        
    Returns:
        Flask JSON response
    """
    response = {
        'success': True,
        'status_code': status_code
    }
    
    if message:
        response['message'] = message
    
    if data is not None:
        response['data'] = data
    
    return jsonify(response), status_code

def error_response(message, status_code=400, error_detail=None):
    """
    Create a standardized error response
    
    Args:
        message: Error message
        status_code: HTTP status code
        error_detail: Additional error details
        
    Returns:
        Flask JSON response
    """
    response = {
        'success': False,
        'status_code': status_code,
        'error': message
    }
    
    if error_detail:
        response['error_detail'] = error_detail
    
    return jsonify(response), status_code