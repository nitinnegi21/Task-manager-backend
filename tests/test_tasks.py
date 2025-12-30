# tests/test_tasks.py - Task endpoint tests
import pytest
import json

class TestHealthCheck:
    """Test health check endpoint"""
    
    def test_health_check_success(self, client):
        """Test health check returns success"""
        response = client.get('/api/health')
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['success'] == True
        assert data['data']['status'] == 'healthy'
        assert 'database' in data['data']

class TestCreateTask:
    """Test task creation"""
    
    def test_create_task_success(self, client, sample_task_data):
        """Test creating a task successfully"""
        response = client.post('/api/tasks', json=sample_task_data)
        assert response.status_code == 201
        
        data = response.get_json()
        assert data['success'] == True
        assert data['message'] == 'Task created successfully'
        assert data['data']['title'] == sample_task_data['title']
        assert data['data']['priority'] == sample_task_data['priority']
        assert 'id' in data['data']
    
    def test_create_task_without_title(self, client):
        """Test creating task without title fails"""
        response = client.post('/api/tasks', json={
            'description': 'No title task'
        })
        assert response.status_code == 400
        
        data = response.get_json()
        assert data['success'] == False
        assert 'Title is required' in data['error_detail']
    
    def test_create_task_invalid_priority(self, client):
        """Test creating task with invalid priority fails"""
        response = client.post('/api/tasks', json={
            'title': 'Test Task',
            'priority': 'invalid'
        })
        assert response.status_code == 400
        
        data = response.get_json()
        assert data['success'] == False
    
    def test_create_task_with_defaults(self, client):
        """Test creating task uses default values"""
        response = client.post('/api/tasks', json={
            'title': 'Minimal Task'
        })
        assert response.status_code == 201
        
        data = response.get_json()
        assert data['data']['priority'] == 'medium'
        assert data['data']['status'] == 'pending'
        assert data['data']['completed'] == False
        assert data['data']['description'] == ''

class TestGetTasks:
    """Test getting tasks"""
    
    def test_get_empty_tasks_list(self, client):
        """Test getting tasks when none exist"""
        response = client.get('/api/tasks')
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['success'] == True
        assert data['data']['tasks'] == []
        assert data['data']['count'] == 0
    
    def test_get_tasks_list(self, client, create_task):
        """Test getting list of tasks"""
        # Create multiple tasks
        create_task({'title': 'Task 1', 'priority': 'high'})
        create_task({'title': 'Task 2', 'priority': 'low'})
        create_task({'title': 'Task 3', 'priority': 'medium'})
        
        response = client.get('/api/tasks')
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['success'] == True
        assert len(data['data']['tasks']) == 3
    
    def test_filter_tasks_by_priority(self, client, create_task):
        """Test filtering tasks by priority"""
        create_task({'title': 'High Task', 'priority': 'high'})
        create_task({'title': 'Low Task', 'priority': 'low'})
        
        response = client.get('/api/tasks?priority=high')
        assert response.status_code == 200
        
        data = response.get_json()
        assert len(data['data']['tasks']) == 1
        assert data['data']['tasks'][0]['priority'] == 'high'
    
    def test_filter_tasks_by_completion(self, client, create_task):
        """Test filtering tasks by completion status"""
        task = create_task({'title': 'Task to complete'})
        task_id = task['data']['id']
        
        # Toggle completion
        client.patch(f'/api/tasks/{task_id}/toggle')
        
        response = client.get('/api/tasks?completed=true')
        assert response.status_code == 200
        
        data = response.get_json()
        assert len(data['data']['tasks']) == 1
        assert data['data']['tasks'][0]['completed'] == True
    
    def test_pagination(self, client, create_task):
        """Test task pagination"""
        # Create 5 tasks
        for i in range(5):
            create_task({'title': f'Task {i+1}'})
        
        # Get first page with limit 2
        response = client.get('/api/tasks?page=1&limit=2')
        assert response.status_code == 200
        
        data = response.get_json()
        assert len(data['data']['tasks']) == 2
        assert data['data']['page'] == 1
        assert data['data']['limit'] == 2

class TestGetTaskById:
    """Test getting a specific task"""
    
    def test_get_task_by_id_success(self, client, create_task):
        """Test getting task by valid ID"""
        task = create_task()
        task_id = task['data']['id']
        
        response = client.get(f'/api/tasks/{task_id}')
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['success'] == True
        assert data['data']['id'] == task_id
    
    def test_get_task_by_invalid_id(self, client):
        """Test getting task with invalid ID format"""
        response = client.get('/api/tasks/invalid-id')
        assert response.status_code == 400
        
        data = response.get_json()
        assert data['success'] == False
        assert 'Invalid task ID' in data['error']
    
    def test_get_nonexistent_task(self, client):
        """Test getting task that doesn't exist"""
        fake_id = '507f1f77bcf86cd799439011'
        response = client.get(f'/api/tasks/{fake_id}')
        assert response.status_code == 404
        
        data = response.get_json()
        assert data['success'] == False
        assert 'not found' in data['error'].lower()

class TestUpdateTask:
    """Test updating tasks"""
    
    def test_update_task_success(self, client, create_task):
        """Test updating task successfully"""
        task = create_task()
        task_id = task['data']['id']
        
        update_data = {
            'title': 'Updated Title',
            'priority': 'low',
            'status': 'in_progress'
        }
        
        response = client.put(f'/api/tasks/{task_id}', json=update_data)
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['success'] == True
        assert data['data']['title'] == 'Updated Title'
        assert data['data']['priority'] == 'low'
        assert data['data']['status'] == 'in_progress'
    
    def test_update_task_partial(self, client, create_task):
        """Test partial update of task"""
        task = create_task({'title': 'Original', 'priority': 'high'})
        task_id = task['data']['id']
        
        response = client.put(f'/api/tasks/{task_id}', json={
            'title': 'Updated'
        })
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['data']['title'] == 'Updated'
        assert data['data']['priority'] == 'high'  # Unchanged
    
    def test_update_nonexistent_task(self, client):
        """Test updating task that doesn't exist"""
        fake_id = '507f1f77bcf86cd799439011'
        response = client.put(f'/api/tasks/{fake_id}', json={
            'title': 'Updated'
        })
        assert response.status_code == 404
    
    def test_update_task_empty_title(self, client, create_task):
        """Test updating task with empty title fails"""
        task = create_task()
        task_id = task['data']['id']
        
        response = client.put(f'/api/tasks/{task_id}', json={
            'title': ''
        })
        assert response.status_code == 400

class TestDeleteTask:
    """Test deleting tasks"""
    
    def test_delete_task_success(self, client, create_task):
        """Test deleting task successfully"""
        task = create_task()
        task_id = task['data']['id']
        
        response = client.delete(f'/api/tasks/{task_id}')
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['success'] == True
        assert 'deleted successfully' in data['message']
        
        # Verify task is deleted
        get_response = client.get(f'/api/tasks/{task_id}')
        assert get_response.status_code == 404
    
    def test_delete_nonexistent_task(self, client):
        """Test deleting task that doesn't exist"""
        fake_id = '507f1f77bcf86cd799439011'
        response = client.delete(f'/api/tasks/{fake_id}')
        assert response.status_code == 404
    
    def test_delete_invalid_id(self, client):
        """Test deleting task with invalid ID"""
        response = client.delete('/api/tasks/invalid-id')
        assert response.status_code == 400

class TestToggleTaskCompletion:
    """Test toggling task completion"""
    
    def test_toggle_task_to_completed(self, client, create_task):
        """Test toggling task to completed"""
        task = create_task()
        task_id = task['data']['id']
        
        response = client.patch(f'/api/tasks/{task_id}/toggle')
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['success'] == True
        assert data['data']['completed'] == True
        assert data['data']['status'] == 'completed'
    
    def test_toggle_task_to_incomplete(self, client, create_task):
        """Test toggling task back to incomplete"""
        task = create_task()
        task_id = task['data']['id']
        
        # Toggle to completed
        client.patch(f'/api/tasks/{task_id}/toggle')
        
        # Toggle back to incomplete
        response = client.patch(f'/api/tasks/{task_id}/toggle')
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['data']['completed'] == False
        assert data['data']['status'] == 'pending'
    
    def test_toggle_nonexistent_task(self, client):
        """Test toggling task that doesn't exist"""
        fake_id = '507f1f77bcf86cd799439011'
        response = client.patch(f'/api/tasks/{fake_id}/toggle')
        assert response.status_code == 404

class TestTaskStatistics:
    """Test task statistics endpoint"""
    
    def test_statistics_empty(self, client):
        """Test statistics with no tasks"""
        response = client.get('/api/tasks/stats')
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['success'] == True
        assert data['data']['total_tasks'] == 0
        assert data['data']['completed_tasks'] == 0
    
    def test_statistics_with_tasks(self, client, create_task):
        """Test statistics with multiple tasks"""
        # Create tasks with different priorities
        create_task({'title': 'High 1', 'priority': 'high'})
        create_task({'title': 'High 2', 'priority': 'high'})
        create_task({'title': 'Medium 1', 'priority': 'medium'})
        create_task({'title': 'Low 1', 'priority': 'low'})
        
        # Complete one task
        task = create_task({'title': 'To Complete'})
        client.patch(f'/api/tasks/{task["data"]["id"]}/toggle')
        
        response = client.get('/api/tasks/stats')
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['data']['total_tasks'] == 5
        assert data['data']['completed_tasks'] == 1
        assert data['data']['pending_tasks'] == 4
        assert data['data']['high_priority_tasks'] == 2
        assert data['data']['medium_priority_tasks'] == 2
        assert data['data']['low_priority_tasks'] == 1