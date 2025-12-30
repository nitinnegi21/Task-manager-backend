# utils/validators.py - Data validation functions
from config import Config

def validate_priority(priority):
    """Validate priority value"""
    return priority in Config.VALID_PRIORITIES

def validate_status(status):
    """Validate status value"""
    return status in Config.VALID_STATUSES

def validate_task_data(data, is_update=False):
    """
    Validate task data
    
    Args:
        data: Dictionary containing task data
        is_update: Boolean indicating if this is an update operation
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Title validation
    if not is_update:
        if 'title' not in data or not data['title']:
            return False, 'Title is required'
        
        if not isinstance(data['title'], str):
            return False, 'Title must be a string'
        
        if len(data['title']) > 200:
            return False, 'Title must be 200 characters or less'
    else:
        if 'title' in data:
            if not data['title']:
                return False, 'Title cannot be empty'
            
            if not isinstance(data['title'], str):
                return False, 'Title must be a string'
            
            if len(data['title']) > 200:
                return False, 'Title must be 200 characters or less'
    
    # Description validation
    if 'description' in data:
        if not isinstance(data['description'], str):
            return False, 'Description must be a string'
        
        if len(data['description']) > 1000:
            return False, 'Description must be 1000 characters or less'
    
    # Priority validation
    if 'priority' in data:
        if not validate_priority(data['priority']):
            return False, f'Priority must be one of: {", ".join(Config.VALID_PRIORITIES)}'
    
    # Status validation
    if 'status' in data:
        if not validate_status(data['status']):
            return False, f'Status must be one of: {", ".join(Config.VALID_STATUSES)}'
    
    # Completed validation
    if 'completed' in data:
        if not isinstance(data['completed'], bool):
            return False, 'Completed must be a boolean'
    
    return True, None