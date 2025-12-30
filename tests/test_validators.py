# tests/test_validators.py - Validator tests
import pytest
from utils.validators import validate_task_data, validate_priority, validate_status

class TestValidatePriority:
    """Test priority validation"""
    
    def test_valid_priorities(self):
        """Test valid priority values"""
        assert validate_priority('low') == True
        assert validate_priority('medium') == True
        assert validate_priority('high') == True
    
    def test_invalid_priorities(self):
        """Test invalid priority values"""
        assert validate_priority('invalid') == False
        assert validate_priority('LOW') == False
        assert validate_priority('') == False
        assert validate_priority(None) == False

class TestValidateStatus:
    """Test status validation"""
    
    def test_valid_statuses(self):
        """Test valid status values"""
        assert validate_status('pending') == True
        assert validate_status('in_progress') == True
        assert validate_status('completed') == True
    
    def test_invalid_statuses(self):
        """Test invalid status values"""
        assert validate_status('invalid') == False
        assert validate_status('PENDING') == False
        assert validate_status('') == False
        assert validate_status(None) == False

class TestValidateTaskData:
    """Test task data validation"""
    
    def test_valid_task_data_create(self):
        """Test valid task data for creation"""
        data = {
            'title': 'Test Task',
            'description': 'Test description',
            'priority': 'high',
            'status': 'pending'
        }
        is_valid, error = validate_task_data(data, is_update=False)
        assert is_valid == True
        assert error is None
    
    def test_valid_task_data_minimal(self):
        """Test valid minimal task data"""
        data = {'title': 'Test Task'}
        is_valid, error = validate_task_data(data, is_update=False)
        assert is_valid == True
        assert error is None
    
    def test_missing_title_create(self):
        """Test missing title for creation"""
        data = {'description': 'No title'}
        is_valid, error = validate_task_data(data, is_update=False)
        assert is_valid == False
        assert 'Title is required' in error
    
    def test_empty_title_create(self):
        """Test empty title for creation"""
        data = {'title': ''}
        is_valid, error = validate_task_data(data, is_update=False)
        assert is_valid == False
        assert 'Title is required' in error
    
    def test_empty_title_update(self):
        """Test empty title for update"""
        data = {'title': ''}
        is_valid, error = validate_task_data(data, is_update=True)
        assert is_valid == False
        assert 'Title cannot be empty' in error
    
    def test_title_too_long(self):
        """Test title exceeding max length"""
        data = {'title': 'x' * 201}
        is_valid, error = validate_task_data(data, is_update=False)
        assert is_valid == False
        assert '200 characters' in error
    
    def test_description_too_long(self):
        """Test description exceeding max length"""
        data = {
            'title': 'Test',
            'description': 'x' * 1001
        }
        is_valid, error = validate_task_data(data, is_update=False)
        assert is_valid == False
        assert '1000 characters' in error
    
    def test_invalid_priority(self):
        """Test invalid priority value"""
        data = {
            'title': 'Test',
            'priority': 'invalid'
        }
        is_valid, error = validate_task_data(data, is_update=False)
        assert is_valid == False
        assert 'Priority must be one of' in error
    
    def test_invalid_status(self):
        """Test invalid status value"""
        data = {
            'title': 'Test',
            'status': 'invalid'
        }
        is_valid, error = validate_task_data(data, is_update=False)
        assert is_valid == False
        assert 'Status must be one of' in error
    
    def test_invalid_completed_type(self):
        """Test invalid completed value type"""
        data = {
            'title': 'Test',
            'completed': 'yes'
        }
        is_valid, error = validate_task_data(data, is_update=False)
        assert is_valid == False
        assert 'Completed must be a boolean' in error
    
    def test_valid_update_partial(self):
        """Test valid partial update"""
        data = {'priority': 'low'}
        is_valid, error = validate_task_data(data, is_update=True)
        assert is_valid == True
        assert error is None
    
    def test_title_not_string(self):
        """Test title is not a string"""
        data = {'title': 123}
        is_valid, error = validate_task_data(data, is_update=False)
        assert is_valid == False
        assert 'Title must be a string' in error
    
    def test_description_not_string(self):
        """Test description is not a string"""
        data = {
            'title': 'Test',
            'description': 123
        }
        is_valid, error = validate_task_data(data, is_update=False)
        assert is_valid == False
        assert 'Description must be a string' in error