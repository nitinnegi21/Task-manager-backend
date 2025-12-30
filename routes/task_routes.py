# routes/task_routes.py - Task API routes
from flask import Blueprint, request, jsonify
from models.task import Task
from utils.validators import validate_task_data, validate_priority, validate_status
from utils.response import success_response, error_response
import logging

logger = logging.getLogger(__name__)

task_bp = Blueprint('tasks', __name__)

@task_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        from database import Database
        Database.client.admin.command('ping')
        
        return success_response(
            data={
                'status': 'healthy',
                'message': 'Task Management API is running',
                'database': 'MongoDB connected'
            }
        )
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return error_response(
            message='Database connection failed',
            status_code=500,
            error_detail=str(e)
        )

@task_bp.route('/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks with optional filtering and pagination"""
    try:
        # Build query from parameters
        query = {}
        
        # Filter by completion status
        completed = request.args.get('completed')
        if completed is not None:
            query['completed'] = completed.lower() == 'true'
        
        # Filter by priority
        priority = request.args.get('priority')
        if priority:
            if not validate_priority(priority):
                return error_response(
                    message='Invalid priority value',
                    status_code=400,
                    error_detail='Priority must be low, medium, or high'
                )
            query['priority'] = priority
        
        # Filter by status
        status = request.args.get('status')
        if status:
            if not validate_status(status):
                return error_response(
                    message='Invalid status value',
                    status_code=400,
                    error_detail='Status must be pending, in_progress, or completed'
                )
            query['status'] = status
        
        # Pagination
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 20))
        skip = (page - 1) * limit
        
        # Sorting
        sort_by = request.args.get('sort_by', 'created_at')
        sort_order = -1 if request.args.get('sort_order', 'desc') == 'desc' else 1
        
        # Get tasks
        tasks = Task.find_all(
            filters=query,
            sort_by=sort_by,
            sort_order=sort_order,
            skip=skip,
            limit=limit
        )
        
        serialized_tasks = [Task.serialize(task) for task in tasks]
        
        return success_response(
            data={
                'tasks': serialized_tasks,
                'page': page,
                'limit': limit,
                'count': len(serialized_tasks)
            }
        )
        
    except Exception as e:
        logger.error(f"Error getting tasks: {str(e)}")
        return error_response(
            message='Failed to retrieve tasks',
            status_code=500,
            error_detail=str(e)
        )

@task_bp.route('/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
    """Get a specific task by ID"""
    try:
        task = Task.find_by_id(task_id)
        
        if not task:
            return error_response(
                message='Task not found',
                status_code=404
            )
        
        return success_response(data=Task.serialize(task))
        
    except ValueError as e:
        return error_response(
            message='Invalid task ID format',
            status_code=400,
            error_detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error getting task {task_id}: {str(e)}")
        return error_response(
            message='Failed to retrieve task',
            status_code=500,
            error_detail=str(e)
        )

@task_bp.route('/tasks', methods=['POST'])
def create_task():
    """Create a new task"""
    try:
        data = request.get_json()
        
        if not data:
            return error_response(
                message='No data provided',
                status_code=400
            )
        
        # Validate task data
        is_valid, error_msg = validate_task_data(data, is_update=False)
        if not is_valid:
            return error_response(
                message='Validation error',
                status_code=400,
                error_detail=error_msg
            )
        
        # Create task
        task = Task.create(data)
        
        logger.info(f"Task created successfully: {task['_id']}")
        
        return success_response(
            data=Task.serialize(task),
            message='Task created successfully',
            status_code=201
        )
        
    except ValueError as e:
        return error_response(
            message='Validation error',
            status_code=400,
            error_detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error creating task: {str(e)}")
        return error_response(
            message='Failed to create task',
            status_code=500,
            error_detail=str(e)
        )

@task_bp.route('/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    """Update an existing task"""
    try:
        data = request.get_json()
        
        if not data:
            return error_response(
                message='No data provided',
                status_code=400
            )
        
        # Validate task data
        is_valid, error_msg = validate_task_data(data, is_update=True)
        if not is_valid:
            return error_response(
                message='Validation error',
                status_code=400,
                error_detail=error_msg
            )
        
        # Update task
        task = Task.update(task_id, data)
        
        if not task:
            return error_response(
                message='Task not found',
                status_code=404
            )
        
        logger.info(f"Task updated successfully: {task_id}")
        
        return success_response(
            data=Task.serialize(task),
            message='Task updated successfully'
        )
        
    except ValueError as e:
        return error_response(
            message='Validation error',
            status_code=400,
            error_detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error updating task {task_id}: {str(e)}")
        return error_response(
            message='Failed to update task',
            status_code=500,
            error_detail=str(e)
        )

@task_bp.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task"""
    try:
        deleted = Task.delete(task_id)
        
        if not deleted:
            return error_response(
                message='Task not found',
                status_code=404
            )
        
        logger.info(f"Task deleted successfully: {task_id}")
        
        return success_response(
            message=f'Task {task_id} deleted successfully'
        )
        
    except ValueError as e:
        return error_response(
            message='Invalid task ID format',
            status_code=400,
            error_detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error deleting task {task_id}: {str(e)}")
        return error_response(
            message='Failed to delete task',
            status_code=500,
            error_detail=str(e)
        )

@task_bp.route('/tasks/<task_id>/toggle', methods=['PATCH'])
def toggle_task_completion(task_id):
    """Toggle task completion status"""
    try:
        task = Task.toggle_completion(task_id)
        
        if not task:
            return error_response(
                message='Task not found',
                status_code=404
            )
        
        logger.info(f"Task completion toggled: {task_id}")
        
        return success_response(
            data=Task.serialize(task),
            message='Task completion status updated'
        )
        
    except ValueError as e:
        return error_response(
            message='Invalid task ID format',
            status_code=400,
            error_detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error toggling task {task_id}: {str(e)}")
        return error_response(
            message='Failed to toggle task completion',
            status_code=500,
            error_detail=str(e)
        )

@task_bp.route('/tasks/stats', methods=['GET'])
def get_task_stats():
    """Get task statistics"""
    try:
        stats = Task.get_statistics()
        
        return success_response(data=stats)
        
    except Exception as e:
        logger.error(f"Error getting task statistics: {str(e)}")
        return error_response(
            message='Failed to retrieve statistics',
            status_code=500,
            error_detail=str(e)
        )