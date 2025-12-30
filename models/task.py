# models/task.py - Task model and data operations
from datetime import datetime
from bson import ObjectId
from bson.errors import InvalidId
from database import Database
import logging

logger = logging.getLogger(__name__)

class Task:
    """Task model for database operations"""
    
    COLLECTION_NAME = 'tasks'
    
    @staticmethod
    def serialize(task):
        """Convert MongoDB document to JSON serializable format"""
        if not task:
            return None
        
        return {
            'id': str(task['_id']),
            'title': task.get('title', ''),
            'description': task.get('description', ''),
            'completed': task.get('completed', False),
            'priority': task.get('priority', 'medium'),
            'status': task.get('status', 'pending'),
            'due_date': task['due_date'].isoformat() if task.get('due_date') else None,
            'created_at': task['created_at'].isoformat() if task.get('created_at') else None,
            'updated_at': task['updated_at'].isoformat() if task.get('updated_at') else None
        }
    
    @staticmethod
    def get_collection():
        """Get tasks collection"""
        return Database.get_collection(Task.COLLECTION_NAME)
    
    @staticmethod
    def validate_id(task_id):
        """Validate MongoDB ObjectId"""
        if not ObjectId.is_valid(task_id):
            raise ValueError("Invalid task ID format")
        return ObjectId(task_id)
    
    @staticmethod
    def create(data):
        """Create a new task"""
        try:
            collection = Task.get_collection()
            
            # Parse due_date if provided
            due_date = None
            if data.get('due_date'):
                try:
                    due_date = datetime.fromisoformat(data['due_date'].replace('Z', '+00:00'))
                except ValueError:
                    raise ValueError('Invalid due_date format. Use ISO format')
            
            # Create task document
            task_doc = {
                'title': data['title'],
                'description': data.get('description', ''),
                'completed': data.get('completed', False),
                'priority': data.get('priority', 'medium'),
                'status': data.get('status', 'pending'),
                'due_date': due_date,
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            }
            
            # Insert task
            result = collection.insert_one(task_doc)
            logger.info(f"Task created with ID: {result.inserted_id}")
            
            # Return created task
            return collection.find_one({'_id': result.inserted_id})
            
        except Exception as e:
            logger.error(f"Error creating task: {str(e)}")
            raise
    
    @staticmethod
    def find_all(filters=None, sort_by='created_at', sort_order=-1, skip=0, limit=20):
        """Find all tasks with optional filtering and pagination"""
        try:
            collection = Task.get_collection()
            query = filters or {}
            
            cursor = collection.find(query).sort(sort_by, sort_order).skip(skip).limit(limit)
            tasks = [task for task in cursor]
            
            logger.info(f"Retrieved {len(tasks)} tasks")
            return tasks
            
        except Exception as e:
            logger.error(f"Error finding tasks: {str(e)}")
            raise
    
    @staticmethod
    def find_by_id(task_id):
        """Find a task by ID"""
        try:
            collection = Task.get_collection()
            object_id = Task.validate_id(task_id)
            
            task = collection.find_one({'_id': object_id})
            
            if task:
                logger.info(f"Task found: {task_id}")
            else:
                logger.warning(f"Task not found: {task_id}")
            
            return task
            
        except ValueError as e:
            logger.error(f"Invalid task ID: {task_id}")
            raise
        except Exception as e:
            logger.error(f"Error finding task: {str(e)}")
            raise
    
    @staticmethod
    def update(task_id, data):
        """Update an existing task"""
        try:
            collection = Task.get_collection()
            object_id = Task.validate_id(task_id)
            
            # Build update document
            update_doc = {'updated_at': datetime.utcnow()}
            
            # Update fields if provided
            allowed_fields = ['title', 'description', 'completed', 'priority', 'status', 'due_date']
            
            for field in allowed_fields:
                if field in data:
                    if field == 'due_date' and data[field]:
                        try:
                            update_doc[field] = datetime.fromisoformat(data[field].replace('Z', '+00:00'))
                        except ValueError:
                            raise ValueError('Invalid due_date format. Use ISO format')
                    else:
                        update_doc[field] = data[field]
            
            # Update task
            result = collection.update_one(
                {'_id': object_id},
                {'$set': update_doc}
            )
            
            if result.matched_count == 0:
                logger.warning(f"Task not found for update: {task_id}")
                return None
            
            logger.info(f"Task updated: {task_id}")
            
            # Return updated task
            return collection.find_one({'_id': object_id})
            
        except ValueError as e:
            logger.error(f"Validation error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error updating task: {str(e)}")
            raise
    
    @staticmethod
    def delete(task_id):
        """Delete a task"""
        try:
            collection = Task.get_collection()
            object_id = Task.validate_id(task_id)
            
            result = collection.delete_one({'_id': object_id})
            
            if result.deleted_count == 0:
                logger.warning(f"Task not found for deletion: {task_id}")
                return False
            
            logger.info(f"Task deleted: {task_id}")
            return True
            
        except ValueError as e:
            logger.error(f"Invalid task ID: {task_id}")
            raise
        except Exception as e:
            logger.error(f"Error deleting task: {str(e)}")
            raise
    
    @staticmethod
    def toggle_completion(task_id):
        """Toggle task completion status"""
        try:
            collection = Task.get_collection()
            object_id = Task.validate_id(task_id)
            
            task = collection.find_one({'_id': object_id})
            
            if not task:
                logger.warning(f"Task not found for toggle: {task_id}")
                return None
            
            new_completed = not task.get('completed', False)
            new_status = 'completed' if new_completed else 'pending'
            
            collection.update_one(
                {'_id': object_id},
                {'$set': {
                    'completed': new_completed,
                    'status': new_status,
                    'updated_at': datetime.utcnow()
                }}
            )
            
            logger.info(f"Task completion toggled: {task_id}")
            
            return collection.find_one({'_id': object_id})
            
        except Exception as e:
            logger.error(f"Error toggling task completion: {str(e)}")
            raise
    
    @staticmethod
    def get_statistics():
        """Get task statistics"""
        try:
            collection = Task.get_collection()
            
            pipeline = [
                {
                    '$facet': {
                        'total': [{'$count': 'count'}],
                        'completed': [
                            {'$match': {'completed': True}},
                            {'$count': 'count'}
                        ],
                        'priority_stats': [
                            {
                                '$group': {
                                    '_id': '$priority',
                                    'count': {'$sum': 1}
                                }
                            }
                        ],
                        'status_stats': [
                            {
                                '$group': {
                                    '_id': '$status',
                                    'count': {'$sum': 1}
                                }
                            }
                        ]
                    }
                }
            ]
            
            result = list(collection.aggregate(pipeline))[0]
            
            total_tasks = result['total'][0]['count'] if result['total'] else 0
            completed_tasks = result['completed'][0]['count'] if result['completed'] else 0
            pending_tasks = total_tasks - completed_tasks
            
            priority_counts = {'low': 0, 'medium': 0, 'high': 0}
            for item in result['priority_stats']:
                priority_counts[item['_id']] = item['count']
            
            status_counts = {'pending': 0, 'in_progress': 0, 'completed': 0}
            for item in result['status_stats']:
                status_counts[item['_id']] = item['count']
            
            logger.info("Task statistics retrieved")
            
            return {
                'total_tasks': total_tasks,
                'completed_tasks': completed_tasks,
                'pending_tasks': pending_tasks,
                'high_priority_tasks': priority_counts['high'],
                'medium_priority_tasks': priority_counts['medium'],
                'low_priority_tasks': priority_counts['low'],
                'status_breakdown': status_counts
            }
            
        except Exception as e:
            logger.error(f"Error getting statistics: {str(e)}")
            raise