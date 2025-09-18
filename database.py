# database.py - MongoDB seeding
from pymongo import MongoClient
from datetime import datetime, timedelta

def init_mongodb():
    """Initialize MongoDB connection and create sample data"""
    try:
        # Connect to MongoDB
        client = MongoClient('mongodb://localhost:27017/')
        db = client.taskmanagement
        tasks_collection = db.tasks
        
        # Check if data already exists
        if tasks_collection.count_documents({}) > 0:
            print("Database already has data. Skipping seed.")
            return
        
        # Sample tasks
        sample_tasks = [
            {
                'title': 'Complete project documentation',
                'description': 'Write comprehensive documentation for the task management system',
                'completed': False,
                'priority': 'high',
                'due_date': datetime.utcnow() + timedelta(days=3),
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            },
            {
                'title': 'Review code changes',
                'description': 'Review pull requests and provide feedback',
                'completed': False,
                'priority': 'medium',
                'due_date': datetime.utcnow() + timedelta(days=1),
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            },
            {
                'title': 'Update dependencies',
                'description': 'Update all project dependencies to latest versions',
                'completed': True,
                'priority': 'low',
                'due_date': None,
                'created_at': datetime.utcnow() - timedelta(days=1),
                'updated_at': datetime.utcnow()
            },
            {
                'title': 'Plan next sprint',
                'description': 'Create tasks and user stories for the next development sprint',
                'completed': False,
                'priority': 'high',
                'due_date': datetime.utcnow() + timedelta(days=7),
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            },
            {
                'title': 'Database backup',
                'description': 'Set up automated database backup system',
                'completed': False,
                'priority': 'medium',
                'due_date': None,
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            }
        ]
        
        # Insert sample tasks
        result = tasks_collection.insert_many(sample_tasks)
        print(f"✅ Successfully added {len(result.inserted_ids)} sample tasks to MongoDB!")
        
        # Create indexes for better performance
        tasks_collection.create_index("completed")
        tasks_collection.create_index("priority")
        tasks_collection.create_index("created_at")
        print("✅ Created database indexes!")
        
        client.close()
        
    except Exception as e:
        print(f"❌ Error initializing MongoDB: {str(e)}")
        print("Make sure MongoDB is running on mongodb://localhost:27017")

if __name__ == '__main__':
    init_mongodb()