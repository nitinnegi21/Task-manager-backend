# tests/conftest.py - Pytest configuration and fixtures
import pytest
from app import create_app
from config import TestingConfig
from database import Database
from models.task import Task

@pytest.fixture(scope='session')
def app():
    """Create application for testing"""
    app = create_app(TestingConfig)
    
    # Setup
    with app.app_context():
        yield app
    
    # Teardown
    Database.close_connection()

@pytest.fixture(scope='function')
def client(app):
    """Create test client"""
    return app.test_client()

@pytest.fixture(scope='function')
def runner(app):
    """Create test CLI runner"""
    return app.test_cli_runner()

@pytest.fixture(scope='function', autouse=True)
def clean_database(app):
    """Clean database before each test"""
    with app.app_context():
        # Clear all tasks before each test
        collection = Task.get_collection()
        collection.delete_many({})
    
    yield
    
    # Clean up after test
    with app.app_context():
        collection = Task.get_collection()
        collection.delete_many({})

@pytest.fixture
def sample_task_data():
    """Sample task data for testing"""
    return {
        'title': 'Test Task',
        'description': 'This is a test task',
        'priority': 'high',
        'status': 'pending',
        'due_date': '2024-12-31T23:59:59'
    }

@pytest.fixture
def create_task(client, sample_task_data):
    """Helper fixture to create a task"""
    def _create_task(data=None):
        task_data = data if data else sample_task_data
        response = client.post('/api/tasks', json=task_data)
        return response.get_json()
    
    return _create_task