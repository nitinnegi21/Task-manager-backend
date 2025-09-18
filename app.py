# app.py - Alternative version using direct PyMongo (no Flask-PyMongo)
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId
from bson.errors import InvalidId
import os

app = Flask(__name__)
CORS(app)

# MongoDB Configuration
MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/')
DATABASE_NAME = 'taskmanagement'

# Initialize MongoDB connection
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
tasks_collection = db.tasks

# Helper function to serialize MongoDB documents
def serialize_task(task):
    """Convert MongoDB document to JSON serializable format"""
    if task:
        return {
            'id': str(task['_id']),
            'title': task['title'],
            'description': task.get('description', ''),
            'completed': task.get('completed', False),
            'priority': task.get('priority', 'medium'),
            'due_date': task['due_date'].isoformat() if task.get('due_date') else None,
            'created_at': task['created_at'].isoformat() if task.get('created_at') else None,
            'updated_at': task['updated_at'].isoformat() if task.get('updated_at') else None
        }
    return None

# Routes
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        # Test MongoDB connection
        client.admin.command('ping')
        return jsonify({
            'status': 'healthy', 
            'message': 'Task Management API is running',
            'database': 'MongoDB connected',
            'database_name': DATABASE_NAME
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Database connection failed',
            'error': str(e)
        }), 500

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks with optional filtering"""
    try:
        # Build query based on parameters
        query = {}
        
        # Filter by completion status
        completed = request.args.get('completed')
        if completed is not None:
            completed_bool = completed.lower() == 'true'
            query['completed'] = completed_bool
        
        # Filter by priority
        priority = request.args.get('priority')
        if priority:
            query['priority'] = priority
        
        # Get tasks from MongoDB
        tasks_cursor = tasks_collection.find(query).sort('created_at', -1)
        tasks = [serialize_task(task) for task in tasks_cursor]
        
        return jsonify(tasks)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
    """Get a specific task by ID"""
    try:
        # Validate ObjectId
        if not ObjectId.is_valid(task_id):
            return jsonify({'error': 'Invalid task ID format'}), 400
            
        task = tasks_collection.find_one({'_id': ObjectId(task_id)})
        
        if not task:
            return jsonify({'error': 'Task not found'}), 404
            
        return jsonify(serialize_task(task))
    
    except InvalidId:
        return jsonify({'error': 'Invalid task ID'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks', methods=['POST'])
def create_task():
    """Create a new task"""
    try:
        data = request.get_json()
        
        if not data or not data.get('title'):
            return jsonify({'error': 'Title is required'}), 400
        
        # Parse due_date if provided
        due_date = None
        if data.get('due_date'):
            try:
                due_date = datetime.fromisoformat(data['due_date'].replace('Z', '+00:00'))
            except ValueError:
                return jsonify({'error': 'Invalid due_date format. Use ISO format'}), 400
        
        # Create task document
        task_doc = {
            'title': data['title'],
            'description': data.get('description', ''),
            'completed': data.get('completed', False),
            'priority': data.get('priority', 'medium'),
            'due_date': due_date,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        # Validate priority
        if task_doc['priority'] not in ['low', 'medium', 'high']:
            return jsonify({'error': 'Priority must be low, medium, or high'}), 400
        
        # Insert task into MongoDB
        result = tasks_collection.insert_one(task_doc)
        
        # Get the created task
        created_task = tasks_collection.find_one({'_id': result.inserted_id})
        
        return jsonify(serialize_task(created_task)), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    """Update an existing task"""
    try:
        # Validate ObjectId
        if not ObjectId.is_valid(task_id):
            return jsonify({'error': 'Invalid task ID format'}), 400
        
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Build update document
        update_doc = {'updated_at': datetime.utcnow()}
        
        # Update fields if provided
        if 'title' in data:
            if not data['title']:
                return jsonify({'error': 'Title cannot be empty'}), 400
            update_doc['title'] = data['title']
        
        if 'description' in data:
            update_doc['description'] = data['description']
        
        if 'completed' in data:
            update_doc['completed'] = bool(data['completed'])
        
        if 'priority' in data:
            if data['priority'] not in ['low', 'medium', 'high']:
                return jsonify({'error': 'Priority must be low, medium, or high'}), 400
            update_doc['priority'] = data['priority']
        
        if 'due_date' in data:
            if data['due_date']:
                try:
                    update_doc['due_date'] = datetime.fromisoformat(data['due_date'].replace('Z', '+00:00'))
                except ValueError:
                    return jsonify({'error': 'Invalid due_date format. Use ISO format'}), 400
            else:
                update_doc['due_date'] = None
        
        # Update task in MongoDB
        result = tasks_collection.update_one(
            {'_id': ObjectId(task_id)},
            {'$set': update_doc}
        )
        
        if result.matched_count == 0:
            return jsonify({'error': 'Task not found'}), 404
        
        # Get updated task
        updated_task = tasks_collection.find_one({'_id': ObjectId(task_id)})
        
        return jsonify(serialize_task(updated_task))
    
    except InvalidId:
        return jsonify({'error': 'Invalid task ID'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task"""
    try:
        # Validate ObjectId
        if not ObjectId.is_valid(task_id):
            return jsonify({'error': 'Invalid task ID format'}), 400
        
        result = tasks_collection.delete_one({'_id': ObjectId(task_id)})
        
        if result.deleted_count == 0:
            return jsonify({'error': 'Task not found'}), 404
        
        return jsonify({'message': f'Task {task_id} deleted successfully'})
    
    except InvalidId:
        return jsonify({'error': 'Invalid task ID'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks/<task_id>/toggle', methods=['PATCH'])
def toggle_task_completion(task_id):
    """Toggle task completion status"""
    try:
        # Validate ObjectId
        if not ObjectId.is_valid(task_id):
            return jsonify({'error': 'Invalid task ID format'}), 400
        
        # Get current task
        task = tasks_collection.find_one({'_id': ObjectId(task_id)})
        
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        
        # Toggle completion status
        new_completed = not task.get('completed', False)
        
        # Update task
        tasks_collection.update_one(
            {'_id': ObjectId(task_id)},
            {'$set': {
                'completed': new_completed,
                'updated_at': datetime.utcnow()
            }}
        )
        
        # Get updated task
        updated_task = tasks_collection.find_one({'_id': ObjectId(task_id)})
        
        return jsonify(serialize_task(updated_task))
    
    except InvalidId:
        return jsonify({'error': 'Invalid task ID'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks/stats', methods=['GET'])
def get_task_stats():
    """Get task statistics"""
    try:
        # Use MongoDB aggregation pipeline
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
                    ]
                }
            }
        ]
        
        result = list(tasks_collection.aggregate(pipeline))[0]
        
        # Parse results
        total_tasks = result['total'][0]['count'] if result['total'] else 0
        completed_tasks = result['completed'][0]['count'] if result['completed'] else 0
        pending_tasks = total_tasks - completed_tasks
        
        # Parse priority stats
        priority_counts = {'low': 0, 'medium': 0, 'high': 0}
        for item in result['priority_stats']:
            priority_counts[item['_id']] = item['count']
        
        return jsonify({
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'pending_tasks': pending_tasks,
            'high_priority_tasks': priority_counts['high'],
            'medium_priority_tasks': priority_counts['medium'],
            'low_priority_tasks': priority_counts['low']
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)